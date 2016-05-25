ff_data_r <- read.delim("~/ff_data_r.txt")
ff_data_ties <- ff_data_r
ff_data_ties$tie <- ifelse(ff_data_ties$away_score==ff_data_ties$home_score,1,0)
homed <- subset(ff_data_ties,select= c(Week,home_team,home_score,max_score,game,tie))
awayd <- subset(ff_data_ties,select = c(Week,away_team,away_score,max_score,game,tie))
homed$win <- ifelse(homed$tie==1,0,ifelse(homed$home_score== homed$max_score,1,0))
homed$loss <- ifelse(homed$tie==1,0,ifelse(homed$home_score != homed$max_score,1,0))
home_win <- aggregate(win ~ home_team, data=homed,sum)
home_loss <- aggregate(loss ~ home_team, data=homed,sum)
home_tie <- aggregate(tie ~ home_team, data=homed,sum)
home_wl <- merge(home_win,home_loss,by="home_team")
home_wlt <- merge(home_wl,home_tie,by="home_team")
awayd$win <- ifelse(awayd$tie==1,0,ifelse(awayd$away_score== awayd$max_score,1,0))
awayd$loss <- ifelse(awayd$tie==1,0,ifelse(awayd$away_score != awayd$max_score,1,0))
away_win <- aggregate(win ~ away_team, data=awayd,sum)
away_loss <- aggregate(loss ~ away_team, data=awayd,sum)
away_tie <- aggregate(tie ~ away_team, data=awayd,sum)
away_wl <- merge(away_win,away_loss,by="away_team")
away_wlt <- merge(away_wl,away_tie,by="away_team")
colnames(home_wlt)[1] <- "team"
colnames(away_wlt)[1] <- "team"
home_wlt$hometeam <- 1
away_wlt$hometeam <- 0
wlt <- rbind(home_wlt,away_wlt)
library("plyr", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")
ddply(wlt,c("team","hometeam"),summarise,wins = sum(win),losses=sum(loss),ties=sum(tie))
