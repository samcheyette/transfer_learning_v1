library(ggplot2)
library(reshape)
library(grid)
library(dplyr)
library(aod)

data <- read.csv("outR.csv")
head(data)


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


###################################################
##############SEQUENCE 2###########################

bin <- 3

m.1 <- data %>% filter(which == 0) %>%
			mutate(timestep2=floor(timestep/bin)+1) %>%
				group_by(subject, timestep2) %>%
				mutate(correct=sum(correct)/bin) %>%

				group_by(timestep2) %>%
				mutate(n_cond=sum(which + 1)) %>%
				mutate(prob_at_time_real=sum(correct)/n_cond) %>%

				mutate(prob_at_time=prob_at_time_real - 0.5) %>%
				group_by(timestep2) %>% 
				top_n(n=1, wt=timestep) %>%
				top_n(n=1, wt=subject)  %>%
				ungroup %>%
				mutate(std_err=((prob_at_time_real * (1-prob_at_time_real)/n_cond)**0.5)) %>%

				select(timestep, timestep2, prob_at_time, consistent, std_err)





m.2 <- data %>% filter(which == 1) %>% 
				mutate(timestep2=floor(timestep/bin)+1) %>%
				group_by(subject, timestep2) %>%
				mutate(correct=sum(correct)/bin) %>%

				group_by(consistent, timestep2) %>%
				mutate(n_cond=sum(which)) %>%
				mutate(prob_at_time_real=sum(correct)/n_cond) %>%

				mutate(prob_at_time=prob_at_time_real - 0.5) %>%
				group_by(timestep2) %>% 
				top_n(n=1, wt=timestep) %>%
				group_by(consistent) %>%
				top_n(1, wt=subject)  %>%
				ungroup %>%
				mutate(std_err=((prob_at_time_real * (1-prob_at_time_real)/n_cond)**0.5)) %>%

				select(timestep, timestep2, prob_at_time, consistent, std_err)
head(m.2)

m.2$consistent <- factor(m.2$consistent)



#p.2 <- ggplot(data=m.2, aes(x=timestep, y=prob_at_time, group=consistent)) +
		#	geom_line(aes(color=consistent))

p.2 <- ggplot(data=m.2, aes(x=timestep2, y=prob_at_time, group=consistent)) +
			geom_bar(stat='identity', position='dodge', aes(fill=consistent)) +
			geom_errorbar(stat='identity', position='dodge',
				aes(ymax=std_err+prob_at_time,
				 ymin=prob_at_time-std_err, group=consistent), 
				size=0.5, alpha=0.6)  +
			geom_point(data=m.1, aes(x=timestep2, y=prob_at_time,
						 colour="Training"), size=4.0)


p.2 <- p.2 +  xlab("Trial bins") + ylab("% above chance") + t1 +
			 scale_x_discrete( expand = waiver(),
			 	limits=c("1-3", "4-6", "7-9", "10-12", "13-15"))  +
			 scale_fill_manual(values=c("#990000", "#009900"),
			 				labels=c("Congruous","Incongruous"))  +
			 scale_color_manual(values=c("#000000"))


ggsave("acc_over_time.pdf", height=9, width=16)



