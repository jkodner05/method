library(ggplot2)

samplings = c("oldicelandic")

for (sampling in samplings){
  data = read.table(paste("~/Documents/Research/Misc/methods/outputs/",sampling,".txt", sep=""), sep="\t", header=TRUE)
  
  
  
  table = table(data$SHORTONLY, data$tolerable)
  pd = data.frame(table(data$TOTAL, data$SHORTONLY, data$tolerable))
  pdt = pd[pd$Var3 == TRUE,]
  ggplot(data=pdt, aes(x=Var1, y=Freq, group=Var2)) +
    geom_line(aes(color=Var2, linetype=Var2), size=1.2) + 
    scale_linetype_manual(values=c("solid","twodash"), labels=c("Class I Weak -j-", "Class I Weak Short-Stem -j-")) + 
    scale_colour_manual(values=c("#56B4E9", "#E69F00"), labels=c("Class I Weak -j-", "Class I Weak Short-Stem -j-")) + 
    theme(legend.title=element_text(size=16), legend.text=element_text(size=14), legend.position="top", axis.title.x = element_text(size=16), axis.text.y = element_text(size=14), axis.title.y = element_text(size=16),  axis.text.x = element_text(size=14, angle = 45, vjust = 0.8)) +
    xlab("Vocabulary Size") +ylab("# Learning Class I Weak Past") + labs(color='Generalization', linetype='Generalization') 
#  ggplot(data=data, aes(x=TOTAL, y=VAL, group=TYPE)) +
#    geom_line(aes(color=TYPE, linetype=TYPE), size=1.2) + 
#    scale_linetype_manual(values=c("solid","twodash", "twodash"), labels=c("N", "e", "theta")) + 
#    scale_colour_manual(values=c("#56B4E9", "#E69F00", "#111111"), labels=c("N", "e", "theta")) + 
#    theme(legend.title=element_text(size=16), legend.text=element_text(size=14), legend.position="top", axis.title.x = element_text(size=16), axis.text.y = element_text(size=14), axis.title.y = element_text(size=16),  axis.text.x = element_text(size=14, angle = 45, vjust = 0.8)) +
#    xlab("Vocabulary Size") +ylab("Tolerability Values") + labs(color='Value', linetype='Value')
  
  ggsave(paste("~/Documents/Research/Misc/methods/outputs/oldicelandic.png", sep=""),
         scale = 1, width = 8, height = 5, units = "in")
  
}