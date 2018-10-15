x11()

#install.packages("ggplot2")

setwd("user/denozi/Programcomparaison")
result<-read.table("result_script.txt", header=FALSE, sep="\t")

write.csv(result, file="graphique.txt")
library("dplyr")
library("ggplot2")
result
#newdata<- result[order(V1),]
#newdata
p<-ggplot(data=result, aes(V3, V2, size=V4, color=V3, label=V4))+ scale_size_area(max_size = 75) + geom_point(data=result, aes(x=V3,y=V2), shape=16) +geom_text(aes(label=V4),hjust=0, vjust=0, size=3, color="black", angle=45) + theme(legend.position = "none") +  ggtitle("Représentation graphique de répartition des phylums pour le génome",V1) + theme(axis.text.x=element_text(angle=45,hjust=1)) + ggtitle("Représentation graphique de répartition des phylums pour le génome",V1) + theme(axis.text.y = element_text(angle=90,hjust=1))+ scale_color_manual(values=c("purple", "gold", "darkturquoise", "green")) +xlab("Phylum")+ylab("Phylum") 