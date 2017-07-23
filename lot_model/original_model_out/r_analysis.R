library(ggplot2)
library(reshape)
library(grid)
library(dplyr)
library(aod)

data <- read.csv("r_analysis.csv")
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


data$congruous <- factor(data$congruous)

##########################################################################

m.1 <- data %>% group_by(model_human, congruous, timestep) %>%
				mutate(id = row_number()) %>%
				mutate(one=1) %>%
				mutate(pcorr=mean(pcorr)) %>%
				top_n(1, wt=id) %>%
				ungroup

bin <- 3

m.1 <- m.1 %>%  group_by(model_human, congruous) %>%
				mutate(timestep2=floor(timestep/bin)+1) %>%
				group_by(id, timestep2, model_human, congruous) %>%
				mutate(pcorr=sum(pcorr)/bin) %>%
				mutate(n_cond=sum(one)) %>%
				mutate(prob_at_time_real=sum(pcorr)/n_cond) %>%

				mutate(prob_at_time=prob_at_time_real - 0.5) %>%
				group_by(timestep2, model_human, congruous) %>% 
				top_n(n=1, wt=timestep) %>%
				mutate(denom= (120.0 + (600 * 
									(1.0 - as.numeric(as.character(congruous)))))) %>%
				mutate(error=(prob_at_time_real *
								 (1.0 - prob_at_time_real)/ 
								 	denom)**0.5) %>%
				mutate(errmin=prob_at_time_real - error,
					   errmax=prob_at_time_real + error ) %>%
				ungroup %>%
				mutate(congruous=c("Incongruent", "Congruent")[as.numeric(congruous)]) %>%
				mutate(model_human=c("Re-use + R-Rules",
					"Human","LOT (Baseline)","Re-use", 
					"Rational Rules")[as.numeric(model_human)]) 

m.1$denom
m.1$error

m.hum <- m.1 %>% filter(grepl("um", model_human))

m.mod <- m.1 %>% filter(!grepl("um", model_human))
m.mod <- m.mod %>% filter(!grepl("Baseline", model_human)) #%>%
			#filter(!grepl("\\+", model_human))




p <- ggplot(m.hum, aes(x=timestep2, y=prob_at_time_real,
				 group=model_human)) +
			#geom_bar(stat='identity', position='dodge') +
			geom_line(size=2.0, 
				aes(linetype="Human           ")) +
			geom_pointrange(aes(ymin=errmin, 
					ymax=errmax)) +

			#geom_point(data=m.mod, aes(x=timestep2, y=prob_at_time_real,
					#		 group=model_human, 
						#	 color=model_human), size=5.0) +
			geom_line(data=m.mod, aes(x=timestep2, y=prob_at_time_real,
							 group=model_human, 
							 color=model_human), 
								size=2.0) +
			facet_wrap(~congruous) +
			ggtitle("Performance by model") +
			 scale_x_discrete( expand = waiver(),
			limits=c("1-3", "4-6", "7-9", "10-12", "13-15"))  +
 			#scale_color_manual(values=c("#914188",
 				#	"#920624", "#113385","#349215")) +
			scale_color_manual(values=c(#"#000000","#F2B429", 
						"#113385","#25B7B4", "#D6B0B0")) +
			scale_linetype_manual(values=c("dotted")) +
 			xlab("Timestep bins") + ylab("Accuracy") +
 			 t1



			#facet_grid(~model_human~congruous)
			#geom_line(aes(color=congruous)) +
			#facet_wrap(~model_human)


ggsave("model_versus_human.png", width=16,height=9)


##############################################################################

m.2 <- data %>% group_by(model_human, congruous) %>%
				mutate(pcorr=mean(pcorr)) %>%
				mutate(id = row_number()) %>%
				top_n(1, wt=id) %>% 
				mutate(is_hum=as.numeric(grepl("um", 
					model_human))) %>%
				mutate(is_cong=as.numeric(as.character(congruous))) %>%
				mutate(error=(pcorr * (1 - pcorr))) %>%
				mutate(error=is_hum * error) %>%
				mutate(error=(error/(120.0*is_cong +
							 600.0 * (1.0 - is_cong)))) %>%
				mutate(error=error**0.5) %>%

				ungroup %>%
				mutate(model_human=c("Re-use + Rational Rules","Human",
					"LOT (Baseline)","Re-use", 
					"Rational Rules")[as.numeric(model_human)]) %>%
				mutate(congruous=c("Incongruent",
				 "Congruent")[as.numeric(congruous)]) 


m.2$error
#p.2 <- ggplot(m.2, aes(x=congruous, y=pcorr, group=model_human)) +
		#	geom_bar(stat='identity', 
					#	position='dodge', aes(fill=model_human)) 
					#+ scale_fill_manual(values=c("#000000", "#349215", "#920624", "#113385")) 
	

m.2 <- m.2 %>% mutate(pcorr = pcorr - 0.5) %>%
		mutate(ymin=pcorr - error, ymax=pcorr+error)


p.2 <- ggplot(m.2, aes(x=model_human, y=pcorr, group=congruous)) +
			geom_bar(stat='identity', 
						position='dodge', 
						aes(fill=congruous)) +
			geom_errorbar(stat='identity', 
				position='dodge', 
				aes(ymin=ymin, ymax=ymax), alpha=0.7) +
			 scale_fill_manual(values=c("#009911", 
			 						"#991100")) +
			 xlab("")  			
 #+ #+
			#facet_wrap(~congruous)

p.2 <- p.2 +
		ylab("% above chance") + t1
m.2

ggsave("sums_models.png", width=16, height=9)