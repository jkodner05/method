library(ggplot2)

samplings = c("isgens")

for (sampling in samplings){
  data = read.table(paste("~/Documents/Research/Misc/methods/outputs/",sampling,".txt", sep=""), sep="\t", header=TRUE)
  
  
#  table = table(data$SGEN, data$tolerable)
  pd = data.frame(table(data$ERA, data$TOTAL, data$GEN, data$TYPE, data$tolerable))
  pdt = pd[pd$Var5 == TRUE,]
pdtj = pdt[pdt$Var3 == "0",]
pdtj1 = pdtj[pdtj$Var4 == "S",]
#  table = table(data$SHORTONLY, data$tolerable)
#  pd = data.frame(table(data$TOTAL, data$SHORTONLY, data$tolerable))
#  pdt = pd[pd$Var3 == TRUE,]
  ggplot(data=pdtj1, aes(x=Var2, y=Freq, group=Var1)) + 
    geom_line(aes(color=Var1, linetype=Var1), size=1.2) + 
    scale_linetype_manual(values=c("solid","twodash"), labels=c("Modern Icelandic", "Old Icelandic")) + 
    scale_colour_manual(values=c("#56B4E9", "#E69F00"), labels=c("Modern Icelandic", "Old Icelandic")) + 
    theme(legend.title=element_text(size=16), legend.text=element_text(size=14), legend.position="top", axis.title.x = element_text(size=16), axis.text.y = element_text(size=14), axis.title.y = element_text(size=16),  axis.text.x = element_text(size=14, angle = 45, vjust = 0.8)) +
    xlab("Vocabulary Size") +ylab("# Learning Monosyllabic Strong") + labs(color='Corpus Era', linetype='Corpus Era') 
#  ggplot(data=data, aes(x=TOTAL, y=VAL, group=TYPE)) +
#    geom_line(aes(color=TYPE, linetype=TYPE), size=1.2) + 
#    scale_linetype_manual(values=c("solid","twodash", "twodash"), labels=c("N", "e", "theta")) + 
#    scale_colour_manual(values=c("#56B4E9", "#E69F00", "#111111"), labels=c("N", "e", "theta")) + 
#    theme(legend.title=element_text(size=16), legend.text=element_text(size=14), legend.position="top", axis.title.x = element_text(size=16), axis.text.y = element_text(size=14), axis.title.y = element_text(size=16),  axis.text.x = element_text(size=14, angle = 45, vjust = 0.8)) +
#    xlab("Vocabulary Size") +ylab("Tolerability Values") + labs(color='Value', linetype='Value')
  
  ggsave(paste("~/Documents/Research/Misc/methods/outputs/oldicelandic.png", sep=""),
         scale = 1, width = 8, height = 5, units = "in")
  
}