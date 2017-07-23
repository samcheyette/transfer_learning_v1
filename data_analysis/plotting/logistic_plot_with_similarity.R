library(ggplot2)
library(reshape)
library(grid)
library(dplyr)
library(aod)
library(lme4)

data <- read.csv("outR_sim.csv")

t0 <- 	theme(axis.text=element_text(size=18), 
		strip.text.x = element_text(size = 20),
		plot.title=element_text(size=18),
		#axis.text.x=element_blank(),
		axis.text.x=element_text(size=15),
		axis.title.x=element_blank(),
		axis.title.y=element_text(size=18),
		axis.text.y=element_text(size=16),

		legend.title=element_blank(),
		legend.text=element_text(size=17),
		 legend.key.size = unit(4, 'lines'))

t001 <- 	theme(axis.text=element_text(size=18), 
		strip.text.x = element_text(size = 20),
		plot.title=element_text(size=18),
		#axis.text.x=element_blank(),
		axis.text.x=element_text(size=15),
		axis.title.x=element_text(size=18),
		axis.title.y=element_text(size=18),
		axis.text.y=element_text(size=16),

		legend.title=element_blank(),
		legend.text= element_text(size=17),
		 legend.key.size = unit(4, 'lines'))


t01 <- 	theme(axis.text=element_text(size=18), 
		strip.text.x = element_text(size = 20),
		plot.title=element_text(size=18),
		#axis.text.x=element_blank(),
		axis.text.x=element_blank(),
		axis.title.x=element_text(size=18),
		
		axis.title.y=element_text(size=18),
		axis.text.y=element_text(size=16),

		legend.title=element_blank(),
		legend.text=element_text(size=17),
		 legend.key.size = unit(4, 'lines'))

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
###############################################################


#head(data)

data <- data %>% filter(which==1)
data$condition <- factor(data$condition)
data$prevexp <- factor(data$prevexp)
data$subject <- factor(data$subject)
data$consistent <- factor(data$consistent)
meansim <- mean(data$sim)
meancorr <- mean(data$correct)

m.1 <- data %>% 

		#mutate(sim=sim/5.0) %>%
		mutate(sim=sim-meansim) %>%
		group_by(condition, sim) %>%
		mutate(consistent=c("Incongruent",
				 "Congruent")[as.numeric(as.character(consistent))+1]) %>%
		mutate(meansim=mean(sim)) %>%
		mutate(meancorr=mean(correct)) %>%
		mutate(tot_cond=paste(meancorr + 0.0001015503057,
				paste(condition, prevexp))) %>%

		mutate(std_dev=(((meancorr * (1-meancorr)))/150.0) ** 0.5) %>%
		mutate(mincorr=meancorr-std_dev) %>%
		mutate(maxcorr=meancorr+std_dev) %>%

		ungroup %>%

		mutate(prevexp=gsub("a", "O", 
					as.character(prevexp))) %>%

		mutate(prevexp=gsub("b", "B", 
					as.character(prevexp)))
		group_by(consistent) %>%
		mutate(ymin=mean(sim)-0.5*sd(sim),
		 ymax=mean(sim)+0.5*sd(sim))

#####################################################

bin <- 3

m.0 <- m.1 %>% group_by(tot_cond) %>%
				mutate(one=1) %>%

				mutate(timestep2=floor(timestep/bin)+1) %>%
				group_by(timestep2, tot_cond) %>%
				mutate(n_cond=sum(one)/bin) %>%
				mutate(correct=sum(correct)/(bin*n_cond))%>%
				top_n(n=1, wt=timestep)  %>%


p.001 <- ggplot(m.0, aes(x=timestep2,
		 y=correct, group=condition)) +
		geom_line(aes( color=consistent),
			 size=2.0, alpha=0.5) +
		facet_wrap(~prevexp)

			 #s+ facet_wrap #+
#+
		#facet_wrap(~prev_exp)


p.001 <- p.001 + t001 + xlab("Trial bins") + ylab("Accuracy") +
			 scale_x_discrete( expand = waiver(),
			 	limits=c("1-3", "4-6", "7-9", "10-12", "13-15")) +
			 scale_color_manual(values=c("#009900","#990000"))
		#scale_color_manual(values=c("#44F044","#F04444")) 

ggsave("all_conditions_overtime.png", width=16, height=9)

######################################################


p.01 <- ggplot(m.1, aes(x=tot_cond, y=meancorr)) +
		geom_point() +
		geom_errorbar(alpha=0.2,aes(ymin=mincorr, 
						ymax=maxcorr),
					 width=0.1) +
		xlab("Conditions") + ylab("Accuracy")

p.01 <- p.01 + t01 #+ scale_color_gradient2(low="#F51119",
									#mid = "white",
									# high = "#3922FF")

ggsave("all_conditions.png", width=8, height=7)

p.1 <- ggplot(m.1, aes(x=meansim, y=meancorr, 
				group=consistent)) + 
		geom_point(aes(color=consistent),
					 size=5.0) #+
		#geom_pointrange(aes(ymin=mincorr, ymax=maxcorr,
					#color=consistent),
					# width=0.1)

					 #+
		#geom_smooth(inherit.aes=FALSE, 
			 #aes(x=meansim, y=meancorr), method="glm", 
						#	formula=y~x)

p.1 <- p.1 + t1 +
		xlab("Similarity") +
		ylab("Accuracy") + ylim(0.2,1.0) +
		scale_color_manual(values=c("#30B650","#B25040"),
			 				labels=c("Congruent", "Incongruent")) 

ggsave("sim_by_ease.png", height=9, width=8)
break
################################################

binomial_smooth <- function(...) {
  geom_smooth(method = "glm", 
  	method.args = list(family = "binomial"), ...)

}


m.2 <- data %>% 
		mutate(sim=sim-meansim) %>%
		mutate(timestep=timestep-7)

mediansim <- median(m.2$sim)
mediansim

m.2 <- m.2 %>% 

		group_by(sim) %>%
		mutate(split=(sim > mediansim))

m.2$consistent <- factor(m.2$consistent)
p.2 <- ggplot(m.2, aes(x=timestep, y=correct, 
						group=split)) +
		geom_jitter(width=0.5, height=0.05, alpha=0.2,
					aes(color=split)) +
		 binomial_smooth(aes(color=split))

p.2

if (FALSE) {
sim.mean <- mean(m.2$sim)
sim.1.below <- sim.mean - sd(m.2$sim)
sim.1.above <- sim.mean + sd(m.2$sim)

mylogit <- glm(data=m.2, formula= correct ~ sim + timestep, 
			   family = binomial(link="logit"))
summary(mylogit)

# Create fake data based on this
fake.data <- data.frame(timestep = rep(range(m.2$timestep), 3),
			sim = c(rep(sim.mean, 2), rep(sim.1.below, 2), rep(sim.1.above, 2)))
# Predict values of self-control
fake.data$correct <- predict(mylogit, fake.data)
head(fake.data)
# Plot!
p.predictions <- ggplot(fake.data, aes(x = timestep, 
				y = correct, color = sim, group = sim)) +
geom_point() +
geom_smooth(method="glm", family=binomial(link="probit"))

p.predictions
}
#p.2
#mylogit <- glmer(formula= correct ~  timestep + consistent + consistent:timestep + (1|subject), 
			 #  data=m, family = binomial(link="logit"))
#ggsave("sim_by_ease.png", height=9, width=16)
####################################################
