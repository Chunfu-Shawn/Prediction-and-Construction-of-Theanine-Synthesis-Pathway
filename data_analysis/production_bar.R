library(ggplot2)
enzyme <- c("CsTS2","CsTSI","BsGS","PtGS","EcGCS")
production <- c(3.99,3.26,9.41,14.76,0.00)
mydata <- data.frame(name=enzyme,production=production)
mydata$name = factor(mydata$name, 
                     levels=c("CsTS2","CsTSI","BsGS","PtGS","EcGCS"))
p<-ggplot(data=mydata,aes(x=name,y = production,fill=production))+
  geom_bar(stat = 'identity',position = "dodge")+
  geom_text(aes(label=production, y=production+0.05), position=position_dodge(0.9), vjust=0) 
p
