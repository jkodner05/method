library(dplyr)
library(reshape2)
library(ggplot2)
library(ggsignif)



  data = read.table(paste("~/Documents/Research/Misc/methods/outputs/","similarities",".txt", sep=""), sep="\t", header=TRUE)
  data <- mutate_if(data, is.character, as.factor)
  data$lexsize = factor(data$lexsize, levels = c("100","500","1042","All"))
  
 # sink("lmsim.txt")
  
  lexsizes = c("100","500","1042","All")
  print(cor(data$jaccard, data$overlap))
  for (lexsize in lexsizes){
    print(lexsize)
    subdata = data[data$lexsize == lexsize,]
    print(cor(subdata$jaccard, subdata$overlap))
  }  


  comtypes = c("inter-cds","inter-non-cds")
  for (comtype in comtypes){
    print(comtype)
    print(levels(lexsize))
    subdata = data[data$comtype == comtype,]
    print(summary(subdata))
#    model.lm <- lm(jaccard ~ lexsize, data = subdata)
#    print(summary(model.lm))
  }

#  data = melt(data, measure.vars = c("jaccard", "overlap"))
levels(data$comptype) = c("CDS and COCA Genre","COCA Inter-Genre")
  p <- ggplot(data, aes(x = lexsize, y = jaccard)) +
    geom_boxplot() 
  p + facet_grid(cols = vars(comptype)) + scale_colour_manual(values=c("#E69F00", "#56B4E9","#E69F00", "#56B4E9")) + labs(color='Corpus Type') +xlab("Comparison Type") +ylab("Jaccard Similarity") +
    theme(strip.text.x=element_text(size=12), axis.title.x = element_text(size=16), axis.title.y = element_text(size=16),  axis.text.x = element_text(size=14, angle = 45, vjust = 0.8), axis.text.y = element_text(size=14))
  #geom_signif(comparisons = list(c("cds", "acad")), annotations="***", y_position = 2.2, tip_length = 0.03)
  

  ggsave(paste("~/Documents/Research/Misc/methods/outputs/allsim.png", sep=""),
       scale = 1, width = 6, height = 4, units = "in")

