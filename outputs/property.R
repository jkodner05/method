library(dplyr)
library(ggplot2)
library(ggsignif)


properties = c("latinate","strongverbs","doubleobj","doubleobjalternators", "irregularverbs")


plotproperties = function(property){
  data = read.table(paste("~/Documents/Research/Misc/methods/outputs/",property,".txt", sep=""), sep="\t", header=TRUE)
  data <- mutate_if(data, is.character, as.factor)
  data$is_adult = data$genre != "cds"
  data$genre <- relevel(data$genre, ref = "cds")
  data$lexsize = factor(data$lexsize, levels = c("100","500","1042","All"))
  
  outfname = paste("~/Documents/Research/Misc/methods/outputs/lm_",property,".txt", sep="")
  sink(outfname)
  
  lexsizes = c("100","500","1042","All")
  for (lexsize in lexsizes){
    print(property)
    print(lexsize)
    subdata = data[data$lexsize == lexsize,]
    model.lm <- lm(typecount ~ is_nonacad, data = subdata)
    print(summary(model.lm))
    model.lm <- lm(typecount ~ genre, data = subdata)
    print(summary(model.lm))
    model.lm <- lm(typecount ~ is_adult, data = subdata)
    print(summary(model.lm))
  }
  
  p <- ggplot(data, aes(x = genre, y = typecount, color=factor(is_adult))) + 
    geom_boxplot() + scale_colour_manual(values=c("#E69F00", "#56B4E9"), labels=c("CHILDES", "COCA")) 
  p + facet_grid(cols = vars(lexsize)) + labs(color='Corpus Type', size=18) +xlab("Genre") +ylab("# Expressing Property") +
      theme(legend.title=element_text(size=16), legend.text=element_text(size=14), strip.text.x=element_text(size=12), legend.position="top", axis.title.x = element_text(size=18), axis.title.y = element_text(size=18),  axis.text.x = element_text(size=16, angle = 90, hjust = 1, vjust = 0.5), axis.text.y = element_text(size=14)) #+
      #geom_signif(comparisons = list(c("cds", "acad")), annotations="***", y_position = 2.2, tip_length = 0.03)
  
  ggsave(paste("~/Documents/Research/Misc/methods/outputs/allprop-",property,".png", sep=""),
         scale = 1, width = 8, height = 5, units = "in")
  
  
q <- ggplot(data, aes(x = is_adult, y = typecount, color=factor(is_adult)),
            add = "jitter") + geom_boxplot() + scale_colour_manual(values=c("#E69F00", "#56B4E9"), labels=c("CHILDES", "COCA")) 
q + facet_grid(cols = vars(lexsize)) + labs(color='Corpus Type') +xlab("Genre") +ylab("# Expressing Property") 
  
#  ggsave(paste("~/Downloads/outputs/cdsprop_",property,".png", sep=""),
#         scale = 1, width = 8, height = 4, units = "in")
  
  #r <- ggplot(data, aes(x = is_nonacad, y = typecount, color=factor(is_nonacad)),
  #            add = "jitter") + geom_boxplot() 
  #r + scale_colour_manual(values=c("#999999", "#56B4E9")) + facet_grid(cols = vars(lexsize)); 
  #ggsave("~/Downloads/outputs/acadproperty.png",
  #       scale = 1, width = 8, height = 4, units = "in")
  

#  data$genre <- relevel(data$genre, ref = "acad")
#  model.lm <- lm(typecount ~ genre, data = subdata)
#  summary(model.lm)
}

for (property in properties){
  plotproperties(property)
}

#boxplot(typecount ~ genre, data = subdata, ylab = "Type Count",  xlab = "Genre")
#boxplot(typecount ~ is_adult, data = subdata, ylab = "Type Count", xlab = "Is Adult Corpus")