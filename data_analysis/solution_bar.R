library(ggplot2)
enzyme <- c("CsTSI","CsTS2","CsAD","BsGS","PtGS","EcGCS","MBP","Keratin","CAPSD")
enzyme2 <- c("CsTSI","MBP-CsTSI","CsAD","MBP-CsAD")
solution <- c(0.047,0.425,0.204,0.304,0.345,0.310,0.325,0.268,0.067)
solution2 <- c(0.047,0.135,0.204,0.261)
mydata <- data.frame(name=enzyme,GRAVY=solution)
mydata$name = factor(mydata$name, 
                     levels=c("CsTSI","CsTS2","CsAD","BsGS","PtGS","EcGCS","MBP","Keratin","CAPSD"))
p<-ggplot(data=mydata,aes(x=name,y = GRAVY,fill=GRAVY))+
  geom_bar(stat = 'identity',position = "dodge")+
  geom_hline(aes(yintercept=0.268),colour="black",linetype="dashed")+
  geom_text(aes(label=GRAVY),vjust=1.5,colour="white")
p

mydata2 <- data.frame(name=enzyme2,GRAVY=solution2)
mydata2$name = factor(mydata2$name, 
                     levels=c("CsTSI","MBP-CsTSI","CsAD","MBP-CsAD"))
p2<-ggplot(data=mydata2,aes(x=name,y = GRAVY,fill=GRAVY))+
  geom_bar(stat = 'identity',position = "dodge",width=0.5)+
  geom_text(aes(label=GRAVY),vjust=1.5,colour="white")
p2
