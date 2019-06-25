library(ggplot2)

samplings = c("irregularverbs_sampled")

for (sampling in samplings){
  data = read.table(paste("~/Documents/Research/Misc/methods/outputs/",sampling,".txt", sep=""), sep="\t", header=TRUE)
  
  
  
  table = table(data$genre, data$prod)
  pd = data.frame(table(data$lexsize, data$genre, data$prod))
  pdt = pd[pd$Var3 == TRUE,]
  ggplot(data=pdt, aes(x=Var1, y=Freq, group=Var2)) +
    geom_line(aes(color=Var2, linetype=Var2), size=1.2) + 
    scale_linetype_manual(values=c("solid","twodash"), labels=c("COCA", "CHILDES")) + 
    scale_colour_manual(values=c("#56B4E9", "#E69F00"), labels=c("COCA", "CHILDES")) + 
    theme(legend.title=element_text(size=16), legend.text=element_text(size=14), legend.position="top", axis.title.x = element_text(size=16), axis.text.y = element_text(size=14), axis.title.y = element_text(size=16),  axis.text.x = element_text(size=14, angle = 45, vjust = 0.8)) +
    xlab("Vocabulary Size") +ylab("# Learning Past +ed") + labs(color='Corpus Type', linetype='Corpus Type')
  
  ggsave(paste("~/Documents/Research/Misc/methods/outputs/samples.png", sep=""),
         scale = 1, width = 8, height = 5, units = "in")
  
  p <- ggplot(data, aes(x = genre, y = typecount, color=genre)) + 
    geom_boxplot() +scale_colour_manual(values=c("#56B4E9", "#E69F00"), labels=c("COCA", "CHILDES")) + 
    geom_point(data=data, aes(x = genre, y = as.numeric(lexsize)/log(as.numeric(lexsize)), color="black"))

  p + facet_grid(cols = vars(lexsize)) + labs(color='Corpus Type') +xlab("Genre") +ylab("# Expressing Property") +
    theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5)) #+
  #  geom_jitter(shape=16, position=position_jitter(0.2)) 
  
  p <- ggplot(data, aes(x = genre, y = as.numeric(lexsize)/log(as.numeric(lexsize)), color=genre)) 
  
  lexsizes = c("100","150","200","250","300","350","400","450","500","550","600","650","700","750","800","850","900","950","1000")
  lexsizes = c("600","650","700","750","800","850","900","950")
#  lexsizes = c("100","500","1000")
#  lexsizes = c("750","750")
  for (lexsize in lexsizes){
    print(sampling)
    print(lexsize)
    subdata = data[data$lexsize == lexsize,]
    table = table(subdata$genre, subdata$prod)
    print(table)
    print(chisq.test(subdata$genre, subdata$prod, correct=TRUE))
  }
}