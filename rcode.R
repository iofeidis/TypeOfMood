library(corrplot)
library(Hmisc)
setwd(dir = 'Documents/Thesis/azuretry2/iOS/DF')

df = read.csv('dfall2020-02-28.csv')
df = subset(df, select = -c(UserID,User_PHQ9))
  
# Pearson
cormat <- round(cor(df, method = "pearson"),2)
corrplot(cormat, method='circle', title = '\n2020-02-28, Pearson')

# Spearman
cormat <- round(cor(df, method = "spearman"),2)
corrplot(cormat, method='circle', title = '\n2020-02-28, Spearman')

df = read.csv('dfall2020-03-02.csv')
df = subset(df, select = -c(UserID,User_PHQ9))

# Pearson
cormat <- round(cor(df, method = "pearson"),2)
corrplot(cormat, method='circle', title = '\n2020-03-02, Pearson')

# Spearman
cormat <- round(cor(df, method = "spearman"),2)
corrplot(cormat, method='circle', title = '\n2020-03-02, Spearman')

df = read.csv('dfall2020-03-14.csv')
df = subset(df, select = -c(UserID,User_PHQ9))

# Pearson
cormat <- round(cor(df, method = "pearson"),2)
corrplot(cormat, method='circle', title = '\n2020-03-14, Pearson')

# Spearman
cormat <- round(cor(df, method = "spearman"),2)
corrplot(cormat, method='circle', title = '\n2020-03-14, Spearman')

# Significance
res2 <- rcorr(as.matrix(df), type='spearman')

pvalues <- subset(res2$P, select = c(Ratio.Stressed.Sad, Ratio.Happy, Ratio.Tired.Sick, Ratio.Relaxed))
#Spearman
pvalues

setwd(dir = 'Documents/Thesis/azuretry2/iOS/85B8C239-2DC0-4D52-A36F-A9B007A9A2A4')

df = read.csv('windows_user.csv')
df = subset(df, select = -c(Window))
df = na.omit(df)

# Pearson
cormat <- round(cor(df, method = "pearson"),2)
corrplot(cormat, method='circle', title = '\n2020-03-14, Pearson')

# Spearman
cormat <- round(cor(df, method = "spearman"),2)
corrplot(cormat, method='circle', title = '\n2020-03-14, Spearman')
