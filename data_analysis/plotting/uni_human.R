library(ggplot2)
library(reshape)
library(grid)
library(dplyr)
library(aod)

t1 <- 	theme(axis.text=element_text(size=15), 
		strip.text.x = element_text(size = 12),
		plot.title=element_text(size=15),
		#axis.text.x=element_blank(),
		axis.text.x=element_text(size=11),
		axis.title.x=element_text(size=12),
		axis.title.y=element_text(size=12),
		axis.text.y=element_text(size=11),

		legend.title=element_blank(),
		legend.text= element_text(size=12),
		 legend.key.size = unit(3, 'lines'))

data <- read.csv("comp_uni.csv")
head(data)
############################################################

bin  <- 3

m.1 <- data %>% group_by(training, transfer) %>%
				mutate(tot_cond=paste(training,transfer)) %>%
				#filter(!grepl("Bigram", who)) %>%
				group_by(tot_cond,is_congruent, who) %>%
				mutate(one=1) %>%

				mutate(time2=floor(time/bin)+1) %>%
				group_by(time2, is_congruent, who) %>%
				mutate(n_cond=sum(one)/bin) %>%

				mutate(corr=sum(corr)/(bin*n_cond))%>%
				top_n(n=1, wt=time2)  %>%
				ungroup

p.1 <- ggplot(m.1, aes(x=time2, y=corr, group=who)) +
			
		geom_line(aes(group=who, color=who, linetype=who), 
			alpha=1.0, size=3.0) +
		 xlab("Trial bins") + ylab("Accuracy") +
			 scale_x_discrete( expand = waiver(),
			 	limits=c("1-3", "4-6", "7-9", "10-12", "13-15")) +
		facet_wrap(~is_congruent)

p.1 <- p.1 + t1 +
		scale_color_manual(values=c("#F1B2C0","#000000",
									 "#B1A190")) + #,
		scale_linetype_manual(values=c("solid","dashed",
									 "solid")) +
		#scale_color_manual(values=c("#000000",
			#						 "#B1A190")) + #,
		#scale_linetype_manual(values=c("dashed",
							#		 "solid"))

ggsave("unigram.png", width=12, height=6)