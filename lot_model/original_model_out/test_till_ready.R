library(ggplot2)
library(reshape)
library(grid)
library(dplyr)
library(aod)

data <- read.csv("r_analysis.csv")
head(data)




t2 <- 	theme(axis.text=element_text(size=10), 
		strip.text.x = element_text(size = 10),
		plot.title=element_text(size=14),
		#axis.text.x=element_blank(),
		axis.text.x=element_text(size=10),
		axis.title.x=element_text(size=13),
		axis.title.y=element_text(size=13),
		axis.text.y=element_text(size=10),

		legend.title=element_blank(),
		legend.text=element_text(size=15),
		 legend.key.size = unit(4, 'lines'))


data$congruous <- factor(data$congruous)

##########################################################################

m.3 <- data %>% group_by(model_human, congruous, transfer, timestep) %>%
				mutate(id = row_number()) %>%
				mutate(one=1) %>%
				mutate(pcorr=mean(pcorr)) %>%
				top_n(1, wt=id) %>%
				group_by(model_human, congruous, transfer) %>%
				ungroup 

bin <- 3

m.3 <- m.3 %>% group_by(model_human, congruous, transfer, timestep) %>%
				mutate(timestep2=floor(timestep/bin)+1) %>%
				group_by(id, timestep2, model_human, congruous, transfer) %>%
				mutate(pcorr=sum(pcorr)/bin) %>%
				mutate(n_cond=sum(one)) %>%
				mutate(prob_at_time_real=sum(pcorr)/n_cond) %>%

				mutate(prob_at_time=prob_at_time_real - 0.5) %>%
				group_by(timestep2, model_human,  congruous, transfer) %>% 
				top_n(n=1, wt=timestep) %>%
				ungroup %>%
				mutate(congruous=c("Incongruent", "Congruent")[as.numeric(congruous)]) %>%
				mutate(model_human=c("Re-Use + Rational Rules", "Human",
							 "LOT (Baseline)", "Re-use",
							 "Rational rules")[as.numeric(model_human)])

#m.3 <- m.3 %>% filter(!grepl("Baseline", model_human))


m.hum <- m.3 %>% filter(grepl("um", model_human))

m.mod <- m.3 %>% filter(!grepl("um", model_human))




p <- ggplot(m.hum, aes(x=timestep2, y=prob_at_time_real,
				 group=model_human)) +
			#geom_bar(stat='identity', position='dodge') +
			geom_line(size=0.5, aes(color=model_human)) +

			geom_point(data=m.mod, aes(x=timestep2, y=prob_at_time_real,
							 group=model_human, 
							 color=model_human), size=3.0) +

			#geom_text(data=m.mod, aes(x=3.0, y=0.1 +
			#			 runif(1,0.1,0.5), 
			#	label=LL, size=2.0, group=model_human))+
			facet_grid(~congruous~transfer) +
			ggtitle("Performance by model") +
			 scale_x_discrete( expand = waiver(),
			 	limits=c("3","6","9","12","15")) +
			#limits=c("1-3", "4-6", "7-9", "10-12", "13-15"))  +
 			scale_color_manual(values=c("#000000", "#F0B241", "#920624", "#113385","#349215")) +
 			xlab("Timestep bins") + ylab("Accuracy") + t2 #+ t1



			#facet_grid(~model_human~congruous)
			#geom_line(aes(color=congruous)) +
			#facet_wrap(~model_human)
ggsave("model_versus_human_largerfacet.pdf", width=24,height=9)

###############################################################
#m.hum <- m.3 %>% filter(grepl("um", model_human))

#m.mod <- m.3 %>% filter(!grepl("um", model_human))


m.4 <- data %>% group_by(model_human, congruous, 
					transfer, timestep) %>%
				mutate(id = row_number()) %>%
				mutate(LL=sum(LL)) %>%
				top_n(1, wt=id) %>%
				ungroup 



#m.4 <- m.4 %>% filter(!grepl("Baseline", model_human))


m.hum <- m.4 %>% filter(grepl("um", model_human))

m.mod <- m.4 %>% filter(!grepl("um", model_human))


f_model <- function(LL, min_LL, model) {
	if (LL == min_LL) {
		ret <- as.character(model)
	} else {
		ret <- ""
	}
	return(ret)
}

m.mod <- m.mod %>% 	

		group_by(model_human, transfer, congruous) %>%
		mutate(LL=sum(LL))  %>%

		top_n(1, wt=timestep)%>% 
		ungroup %>%
		group_by(transfer, congruous) %>%
		mutate(min_LL=max(LL)) %>%
		group_by(model_human, transfer, congruous) %>%
		mutate(is_min = f_model(LL, min_LL, model_human)) %>%
		group_by(model_human) %>%
		mutate(sum_LL=sum(LL))




head(m.mod)
m.mod$is_min

p <- ggplot(m.mod, aes(x=model_human, y=-2.0*LL)) +

			#geom_bar(stat='identity', position='dodge') +
			geom_bar(stat='identity',aes(fill=model_human)) +
			geom_text(aes(x=2.0,y=-20, label="*",
			 color=model_human), size=10.0) +
				#position='dodge', aes(fill=model_human)) +
			 facet_grid(~congruous~transfer, scales="free_y")

#p
ggsave("loglike.pdf", width=24,height=9)
