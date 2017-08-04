library(ggplot2)
library(reshape)
library(grid)
library(dplyr)
library(aod)
library(lme4)

data <- read.csv("outR_trans.csv")


t1 <- 	theme(axis.text=element_text(size=18), 
		strip.text.x = element_text(size = 20),
		plot.title=element_text(size=18),
		#axis.text.x=element_blank(),
		axis.text.x=element_text(size=15),
		axis.title.x=element_text(size=18),
		axis.title.y=element_text(size=18),
		axis.text.y=element_text(size=16),

		legend.title=element_blank(),
		legend.text=element_text(size=17),
		 legend.key.size = unit(4, 'lines'))
##########################################################

m.1 <- data %>%
	   filter(which==1) %>%
	   select(timestep, condition, 
	   	prevexp, ntrans, timestep, correct, subject)






m.1$timestep.centered <- m.1$timestep - mean(m.1$timestep)
m.1$ntrans.centered <- m.1$ntrans - mean(m.1$ntrans)

mylogit <- glm(data=m.1, formula= correct ~ 
									ntrans.centered +
								 timestep.centered, 
			   family = binomial(link="logit"))
summary(mylogit)



######################################################
ntrans.mean <- mean(m.1$ntrans.centered)
ntrans.1.below <- ntrans.mean - 2*sd(m.1$ntrans.centered)
ntrans.1.above <- ntrans.mean + 2*sd(m.1$ntrans.centered)
#rep(range(m.1$timestep.centered), 3)
#rng <- c(-7,-4,0,4,7,-7,-4,0,4,7,-7,-4,0,4,7)
rng <- c(seq(-7,7,3),seq(-7,7,3),seq(-7,7,3))
fake.data <- data.frame(
		timestep.centered = rng,
		ntrans.centered = c(rep(ntrans.mean, 5), 
		rep(ntrans.1.below, 5),
 	rep(ntrans.1.above,5)))

fake.data

fake.data$correct <-
		 predict(mylogit, fake.data, type="response")


head(fake.data)

p.predictions <- ggplot(fake.data, 
		aes(x = ntrans.centered,
		 y = correct, 
		 color = timestep.centered, 
		 group = timestep.centered)) +
		geom_point() +
		geom_line()

ggsave("transformation_predictions.pdf")