rm(list = ls())

setwd("/Users/maxons/Documents/django_projects/Gestion_comptes_django")
chart_folder <- "graphics/"

library(dplyr)
library(lubridate)
library(ggplot2)
# pour aligner les graphiques ggplot
library(grid)
# pour faire multi ggplot2 graph
library(gridExtra)

data <- read.csv("test_csv_pd.csv")

data$type <- factor(data$type, levels = c("Loyer", "Sorties", "Nourriture", "Loisirs", "Charges", "Autre",
                                                    "Ammeublement", "Soin_Hygiene", "Sport", "Vetements", "Voyages", "Salaire"))

# Clean whole dataset
data$date_ope <- as.Date(data$date_ope, "%Y-%m-%d")
day(data$date_ope) <- 1
df_sum_all <- summarise(group_by(data, debit, type, date_ope), total = sum(montant))
df_all <- as.data.frame(df_sum_all)

# Creates dataset with list of all month / dates
df_date_type = merge(as.data.frame(unique(data$type)), as.data.frame(unique(data$date_ope)), by=NULL)
colnames(df_date_type) = c("type", "date_ope")


# Clean for debit
df_deb <- filter(df_all, debit == TRUE)
df_sum_deb <- filter(df_sum_all, debit == TRUE)
# We want to add the month when there is no demand for a type on the month
df_sum_deb_full = select(as.data.frame(right_join(df_sum_deb, df_date_type)), type, date_ope, total)
df_sum_deb_full$total[which(is.na(df_sum_deb_full$total))] = 0


# Clean for credit
df_cre <- filter(df_all, debit == FALSE)
df_sum_cre <- filter(df_sum_all, debit == FALSE)
# We want to add the month when there is no demand for a type on the month
df_sum_cre_full = select(as.data.frame(right_join(df_sum_cre, df_date_type)), type, date_ope, total)
df_sum_cre_full$total[which(is.na(df_sum_cre_full$total))] = 0


# Data for comparing Deb/Cred (CIC like chart at first)
# Build a dataset where cred is > 0 and deb < 0
df_sum_all_t <- df_sum_all
df_sum_all_t[df_sum_all_t$debit == TRUE,]$total <- -df_sum_all_t[df_sum_all_t$debit == TRUE,]$total

# Computes by month the total difference between cred and deb
df_diff_deb_cred <- summarise(group_by(df_sum_all_t, date_ope), diff = sum(total))






# --------------------------------------------------------------------
# Set up colors variables
# --------------------------------------------------------------------

# Set up colors
cols <- c("TRUE" = "#E83F26", "FALSE" = "#28B463")
col_diff = "#26547C"

col_type <- c("Loyer" = "#F8766D", "Sorties" = "#DB8E00", "Nourriture" = "#AEA200", "Loisirs" = "#64B200", 
              "Charges" = "#00BD5C", "Autre" = "#00C1A7", "Ammeublement" = "#00BADE", 
              "Soin_Hygiene" = "#00A6FF", "Sport" = "#B385FF", "Vetements" = "#EF67EB", "Voyages" = "#FF63B6", "Salaire" = "#844D9E")

# --------------------------------------------------------------------
# We plot the demand by type with all months
# --------------------------------------------------------------------

# Plot les budgets un par un avec évolution au cours du temps
# p <- ggplot(data=df_sum_deb_full, aes(x=df_sum_deb_full$date_ope, y=df_sum_deb_full$total, 
#                                 colour=df_sum_deb_full$type, shape=df_sum_deb_full$type))
# p <- p+geom_point(size = 4)
# p <- p + ggtitle("Evolution de ma dépense au cours du temps")
# p <- p + geom_line(size = 1)
# p <- p + xlab("Mois")
# p <- p + ylab("Montant")
# print(p)



# --------------------------------------------------------------------
# We plot the demand by type without months
# --------------------------------------------------------------------
# p <- ggplot(data=df_sum_deb, aes(x=df_sum_deb$date_ope, y=df_sum_deb$total, 
#                                  colour=df_sum_deb$type, shape=df_sum_deb$type))
# p <- p+geom_point(size = 4)
# p <- p + ggtitle("Evolution de ma dépense au cours du temps")
# p <- p + geom_line(size = 2)
# p <- p + xlab("Mois")
# p <- p + ylab("Montant")
# print(p)


# --------------------------------------------------------------------
# We plot the stacked bar chart of the demand
# --------------------------------------------------------------------
df_sum_cre_all <- summarise((group_by(df_cre, date_ope)), total = sum(total))
p <- ggplot(df_sum_deb, aes(date_ope, total))
p <- p + geom_bar(aes(fill = type), stat="identity", position = position_stack(reverse = T)) 
p <- p + scale_fill_manual(values = col_type)
print(p)

ggsave(paste(chart_folder, "stack_debit.png", sep = ""))

# --------------------------------------------------------------------
# We plot the stacked bar chart of the demand with diff cred/deb
# --------------------------------------------------------------------
df_sum_cre_all <- summarise((group_by(df_cre, date_ope)), total = sum(total))
rm(p)
p <- ggplot(df_sum_deb, aes(date_ope, total))
p <- p + geom_bar(aes(fill = type), stat="identity", position = position_stack(reverse = T)) 
#p <- p + geom_hline(yintercept = 2056)
#p <- p + geom_line(data=df_sum_cre_all, aes(x=date_ope, y=total), colour="blue")

p <- p + geom_line(data=df_diff_deb_cred, 
                   aes(x=date_ope, y=diff), colour=col_diff)
p <- p + geom_point(data=df_diff_deb_cred, aes(x=date_ope, y=diff), colour=col_diff)
p <- p + geom_text(data=df_diff_deb_cred, aes(x=date_ope, y=round(diff), label=round(diff))
                   ,hjust=0, vjust=0, colour=col_diff)
p <- p + scale_fill_manual(values = col_type)

print(p)
ggsave(paste(chart_folder, "stack_debit_wdiff.png", sep = ""))


# --------------------------------------------------------------------
# We plot the sum of debit / credit per month
# --------------------------------------------------------------------
# df_sum_all <- summarise((group_by(data, debit, date_ope)), total = sum(montant))
# p <- ggplot(data = df_sum_all, aes(x = df_sum_all$date_ope, y = df_sum_all$total, fill = df_sum_all$debit))
# p <- p + geom_bar(stat="identity", position=position_dodge()) 
# print(p)


# --------------------------------------------------------------------
# Computes for a month the budget spend
# --------------------------------------------------------------------
# Notes: does not take in account the year of the month

# Objectives of June 2017:
# Loyer : 680
# Charges : 115
# Nourriture : 200
# Autre : 60
# Sorties : 115

summary_month <- function(month_)
{
  colToKeep = c("Loyer", "Charges", "Nourriture", "Autre", "Sorties")
  temp = filter(data, month(date_ope) == month_ & debit == TRUE & type %in% colToKeep)
  df = summarise(group_by(temp, type), "total" = sum(montant))
  ind = sapply(colToKeep, function(x) which(df$type == x)[1])
  df[ind[!is.na(ind)],]
}
summary_month(7)
summary_month(8)
summary_month(9)
summary_month(10)
summary_month(11)
summary_month(12)


# --------------------------------------------------------------------
# Stacked bar chart for types with the sub budgets
# --------------------------------------------------------------------

to_keep = c('Ammeublement', 'Soin_Hygiene', 'Sport', 'Voyages', 'Vetements')
data_keeped = df_sum_deb[df_sum_deb$type %in% to_keep,]
#rm(p_sub)
p_sub <- ggplot(data_keeped, aes(date_ope, total))
p_sub <- p_sub + geom_bar(aes(fill = type), stat="identity", position = position_stack(reverse = T))
p_sub <- p_sub + scale_fill_manual(values = col_type)
print(p_sub)

# --------------------------------------------------------------------
# Stacked bar chart for types with the most volatility
# --------------------------------------------------------------------

to_remove = c('Loyer', 'Ammeublement', 'Soin_Hygiene', 'Sport', 'Voyages', 'Vetements')
data_keeped = df_sum_deb[!(df_sum_deb$type %in% to_remove),]
#rm(p_most)
p_most <- ggplot(data_keeped, aes(date_ope, total))
p_most <- p_most + geom_bar(aes(fill = type), stat="identity", position = position_stack(reverse = T))
p_most <- p_most + scale_fill_manual(values = col_type)
print(p_most)


# --------------------------------------------------------------------
# Stacked bar chart for types with all the credits
# --------------------------------------------------------------------

to_remove = c('Salaire')
data_keeped = df_sum_cre[!(df_sum_cre$type %in% to_remove),]
#rm(p_cre)
p_cre <- ggplot(data_keeped, aes(date_ope, total))
p_cre <- p_cre + geom_bar(aes(fill = type), stat="identity", position = position_stack(reverse = T))
p_cre <- p_cre + scale_fill_manual(values = col_type)
print(p_cre)

png(paste(chart_folder, "stack_vol_sub_cred.png", sep = ""), width = 1000, height = 800)
grid.arrange(p_most, p_sub, p_cre, ncol=1, nrow = 3)
dev.off()

# --------------------------------------------------------------------
# Stacked bar chart with for each month the sum volatility/sub
# --------------------------------------------------------------------
to_sub = c('Ammeublement', 'Soin_Hygiene', 'Sport', 'Voyages', 'Vetements')
# 
# col_type <- c("Loyer" = "#00A6FF", "Sorties" = "#FF63B6", "Nourriture" = "#00BADE", "Loisirs" = "#B385FF", 
#               "Charges" = "#EF67EB", "Autre" = "#F8766D", "Ammeublement" = "#DB8E00", 
#               "Soin_Hygiene" = "#AEA200", "Sport" = "#64B200", "Vetements" = "#00BD5C", "Voyages" = "#00C1A7", "Salaire" = "#26547C")
# 
# col_type <- c("Loyer" = "#F8766D", "Sorties" = "#DB8E00", "Nourriture" = "#AEA200", "Loisirs" = "#64B200", 
#               "Charges" = "#00BD5C", "Autre" = "#00C1A7", "Ammeublement" = "#00A6FF", 
#               "Soin_Hygiene" = "#FF63B6", "Sport" = "#00BADE", "Vetements" = "#B385FF", "Voyages" = "#EF67EB", "Salaire" = "#26547C")
# 
# p_dist_deb <- ggplot(for_chart, aes(date_ope, total))
# p_dist_deb <- p_dist_deb + geom_bar(stat="identity", aes(fill = type), position = position_stack(reverse = T)) 
# print(p_dist_deb)
# 
# 
# 
# col_type <- c("Loyer" = "#F8766D", "Sorties" = "#DB8E00", "Nourriture" = "#AEA200", "Loisirs" = "#64B200", 
#               "Charges" = "#00BD5C", "Autre" = "#00C1A7", "Ammeublement" = "#00BADE", 
#               "Soin_Hygiene" = "#00A6FF", "Sport" = "#B385FF", "Vetements" = "#EF67EB", "Voyages" = "#FF63B6", "Salaire" = "#844D9E")

# cols <- c("TRUE" = "#E83F26", "FALSE" = "#28B463")
# p <- p + scale_fill_manual(values = cols)

p_dist_deb <- ggplot(for_chart, aes(date_ope, total))
p_dist_deb <- p_dist_deb + geom_bar(stat="identity", aes(fill = type), position = position_stack(reverse = T)) 
p_dist_deb <- p_dist_deb + scale_fill_manual(values = col_type)
print(p_dist_deb)


# Overall deb / cred
p_dist_deb <- ggplot(for_chart, aes(date_ope, total))
p_dist_deb <- p_dist_deb + geom_bar(stat="identity", aes(fill = type), position = position_stack(reverse = T)) 
# Add the line for difference
p_dist_deb <- p_dist_deb + geom_line(data=df_diff_deb_cred,
                   aes(x=date_ope, y=diff), colour=col_diff)
p_dist_deb <- p_dist_deb + geom_point(data=df_diff_deb_cred, aes(x=date_ope, y=diff), colour=col_diff)

png(paste(chart_folder, "stack_deb_sep_cre.png", sep = ""), width = 1000, height = 800)
grid.draw(rbind(ggplotGrob(p_dist_deb), ggplotGrob(p_cre), size = "last"))
dev.off()
#ggsave(paste(chart_folder, "stack_deb_sep_cre.png", sep = ""), plot = plot_to_save)


g <- ggplot_build(p_dist_deb)
unique(g$data[[1]]["fill"])



# --------------------------------------------------------------------
# Boxplot for types with the most volatility
# --------------------------------------------------------------------
data_keeped$type <- as.character(data_keeped$type)
sum_deb <- summarise(group_by(data_keeped, type, date_ope), total = sum(total))
boxplot( sum_deb$total~ sum_deb$type)


# --------------------------------------------------------------------
# We plot the demand for each budget with the highest volatility
# --------------------------------------------------------------------

# Loyer : 680
# Charges : 115
# Nourriture : 200
# Autre : 60
# Sorties : 115

# Vetements
data_keeped = filter(df_sum_deb_full, type == 'Vetements')
p_Vetements <- ggplot(data_keeped, aes(date_ope, total)) + geom_bar(aes(fill = type), stat="identity") + scale_fill_manual(values = col_type)
#p_Vetements <- p_Vetements + ggtitle("Evolution de ma dépense au cours du temps")

# Sorties
data_keeped = filter(df_sum_deb_full, type == 'Sorties')
p_Sorties <- ggplot(data_keeped, aes(date_ope, total)) + geom_bar(aes(fill = type), stat="identity")  + scale_fill_manual(values = col_type)
p_Sorties <- p_Sorties + ggtitle("Obj: 115")

# Nourriture
data_keeped = filter(df_sum_deb_full, type == 'Nourriture')
p_Nourriture <- ggplot(data_keeped, aes(date_ope, total)) + geom_bar(aes(fill = type), stat="identity")  + scale_fill_manual(values = col_type)
p_Nourriture <- p_Nourriture + ggtitle("Obj: 200")

# Loisirs
data_keeped = filter(df_sum_deb_full, type == 'Loisirs')
p_Loisirs <- ggplot(data_keeped, aes(date_ope, total)) + geom_bar(aes(fill = type), stat="identity")  + scale_fill_manual(values = col_type)
#p_Loisirs <- p_Loisirs + ggtitle("Evolution de ma dépense au cours du temps")

# Charges
data_keeped = filter(df_sum_deb_full, type == 'Charges')
p_Charges <- ggplot(data_keeped, aes(date_ope, total)) + geom_bar(aes(fill = type), stat="identity")  + scale_fill_manual(values = col_type)
p_Charges <- p_Charges + ggtitle("Obj: 115")

# Autre
data_keeped = filter(df_sum_deb_full, type == 'Autre')
p_Autre <- ggplot(data_keeped, aes(date_ope, total)) + geom_bar(aes(fill = type), stat="identity")  + scale_fill_manual(values = col_type)
p_Autre <- p_Autre + ggtitle("Obj: 60")

png(paste(chart_folder, "stack_type_by_type.png", sep = ""), width = 1000, height = 800)
grid.arrange(p_Vetements,p_Sorties, p_Nourriture, p_Charges, p_Loisirs, p_Autre, ncol=3, nrow = 2)
dev.off()

# --------------------------------------------------------------------
# CIC like chart for debit vs credit
# --------------------------------------------------------------------

rm(p)
# Overall deb / cred
p <- ggplot(df_sum_all_t, aes(date_ope, total))
p <- p + geom_bar(aes(fill = debit), stat="identity") 
# Add the line for difference
p <- p + geom_line(data=df_diff_deb_cred, 
                   aes(x=date_ope, y=diff), colour=col_diff)
p <- p + geom_point(data=df_diff_deb_cred, aes(x=date_ope, y=diff), colour=col_diff)
p <- p + geom_text(data=df_diff_deb_cred, aes(x=date_ope, y=round(diff), label=round(diff))
                   ,hjust=0, vjust=0, colour=col_diff)
# Colors for the bar
p <- p + scale_fill_manual(values = cols)
print(p)

ggsave(paste(chart_folder, "stack_overall_deb_cre.png", sep = ""))
