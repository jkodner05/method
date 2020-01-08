library(ggplot2)

data = read.table(paste("~/Documents/Research/Misc/methods/outputs/","saturations",".txt", sep=""), sep="\t", header=TRUE)

types = data[,2:3]
factors = c(1:2)
newcol = rep(0,dim(data)[1])
for(f in factors){
  colvalues=types[,f]
  newcol[which(colvalues==1)]=f
}
data$corptype = as.factor(newcol)

summary(lm(log(meansat) ~ log(pdgmsize) + log(tokentype) + iscds + ishistorical, data = data))
summary(lm(log(meansat) ~ log(pdgmsize), data = data))
summary(lm(log(meansat) ~ log(tokentype), data = data))
summary(lm(meansat ~ pdgmsize + tokentype + iscds + ishistorical, data = data))
summary(lm(meansat ~ pdgmsize, data = data))
summary(lm(meansat ~ tokentype, data = data))
summary(lm(meansat ~ iscds, data = data))

ggplot(data=data, aes(x=log(pdgmsize), y=log(meansat))) + labs(color='Corpus Type') + xlab("log(paradigm size)") + ylab("log(mean saturation)") +
  geom_point(aes(color=corptype), size=2.5) +scale_colour_manual(values=c("#56B4E9", "#E69F00", "#999999"), labels=c("UDT-Modern", "CHILDES-CDS", "UDT-Historical")) + 
  geom_smooth(method='lm', formula=y~x, se=FALSE, color = "black")
ggsave(paste("~/Documents/Research/Misc/methods/outputs/saturation.png", sep=""),
       scale = 1, width = 8, height = 4, units = "in")

