
library(ggplot2)
library(dplyr)
library(reshape)
library(hash)


t1 <- 	theme(axis.text=element_text(size=18), 
		strip.text.x = element_text(size = 24),
		plot.title=element_text(size=20),
		axis.text.x=element_blank(),
		#axis.text.x=element_text(size=20, angle=45),

		#axis.title.x=element_text(size=13),
		axis.title.y=element_text(size=20),

		axis.title.x=element_blank(),
		axis.text.y=element_text(size=17),

		legend.title=element_blank(),
		legend.text=element_text(size=17),
		 legend.key.size = unit(6, 'lines'))



BURNIN <- 10000

header_f <- read.csv("header.csv")
header <- colnames(header_f)

#full <- "100100010000100000100000010000"

#s1 <- "100100010000100"
s1 <-  "010110101101011"
#s1 <- "000000111111111"
#s1 <- "001001001001001"
#s1 <- "111110101010101"
#s1 <- "110001100011000"

s2 <-  s1
s1_tr <- "train_"
s2_tr <- "trans_"
f1 <- paste(s1_tr, s1, sep="")
f2 <- paste(s2_tr, s2, sep="")

dwide1 <- read.table(paste(s1_tr, 
		paste(s1, ".txt", sep=""), sep=""), 
				header=F)
dwide2 <- read.table(paste(s2_tr, 
					paste(s2, ".txt", sep=""), sep=""), 
					header=F)


colnames(dwide1) <- header
colnames(dwide2) <- header
colnames(dwide1)[ncol(dwide1)] <- s1
colnames(dwide2)[ncol(dwide2)] <- s1

dwide1 <- dwide1  %>% mutate(which=factor(f1)) %>% 
					filter(steps < 100000)
dwide2 <- dwide2 %>% mutate(which=factor(f2)) %>% 
					 filter(steps < 100000) 
dwide <- rbind(dwide1, dwide2)

#weird problem...

m <- melt(dwide, c("steps", "chain", "which"))
m <- m %>% filter(!grepl("temp", as.character(variable))) %>%
			filter(!grepl("posterior",as.character(variable))) %>%
			filter(!grepl("proposal",as.character(variable))) %>%
			filter(!grepl("alpha",as.character(variable))) %>%
			filter(!grepl("beta",as.character(variable))) %>%
			mutate(variable=gsub("25", "INFINITY", variable))


m$chain <- factor(m$chain)
m <- m %>% filter(steps %% 100 == 0) %>%
			filter(steps > BURNIN)
 #%>%
			#filter(grepl(s1, variable) | grepl(s2, variable) |
				#(nchar(as.character(variable)) < 19))

#########################################################
#if(FALSE) {
m.1 <- m %>% filter(steps %% 1000 == 0)%>% 
		filter(grepl("trans", which)) %>%

		filter(!grepl("INT", variable)) %>%
		mutate(which=gsub("0", "", which)) %>%
		mutate(which=gsub("1", "", which))

#plt.1 <- ggplot(data=m.1, aes(x=steps, y=value,group=chain)) +
	#	geom_line(aes(x=steps, y=value, color=chain)) +
	#	facet_wrap(~variable~which) + ylim(0,1)

plt.1 <- ggplot(data=m.1, aes(x=steps, y=value,group=chain)) +
		geom_line(aes(x=steps, y=value, color=chain)) +
		facet_wrap(~variable) + ylim(0,1)

ggsave("MCMC_chains.pdf", width=30, height=12)
#}
#############################################################


m.2 <- m %>%
		filter(!grepl("INT", variable)) %>%
		group_by(which, chain, variable) %>%
		mutate(mean_p = mean(value)) %>%
		group_by(which, variable) %>%
		mutate(mean_p = mean(mean_p)) %>%

		top_n(n=1, wt=steps+as.numeric(as.character(chain))) %>%


		#top_n(n=1, wt=steps+as.numeric(as.character(chain))) %>%
		#use when delete above ^

		group_by(variable) %>%
		mutate(sum_p=sum(mean_p)) %>%
		ungroup %>%
		mutate(variable=gsub("TERM_","", variable)) %>%
		mutate(variable=gsub("0", "O", 
				variable)) %>%
		mutate(variable=gsub("1", "B", 
				variable)) %>%

		mutate(variable=substr(variable, 1,9)) %>%

		#mutate(variable=gsub(paste(s1, "s1", sep=""),"OBOBB...", variable)) %>%
		#mutate(variable=gsub("1","O", variable)) %>%
		mutate(which=gsub(s1,"", which)) %>%
		mutate(which=gsub("_","", which)) %>%
		mutate(which=gsub("train", "Training", which)) %>%
		mutate(which=gsub("trans", "Transfer", which)) %>%

		filter(nchar(as.character(variable)) > 4) %>%
		mutate(variable=gsub("from_n","cut", variable)) %>%
		mutate(variable=toupper(variable)) %>%
		transform(variable=factor(reorder(variable, -sum_p))) %>%

		group_by(which) %>%
		mutate(mean_p = mean_p/sum(mean_p)) 


head(m.2)

plt.2 <- ggplot(data=m.2, aes(x=variable, y=mean_p,
				group=which)) +
			geom_bar(stat='identity',
				 position='dodge', 
				 aes(fill=which)) + #,
				 	#alpha=1.0-as.numeric(as.factor(which)))) +
				 	 t1 +
			geom_text(data=m.2, aes(x=variable, y=-0.01, 
							label=variable), size=6.0,
							angle=0)

plt.2 <- plt.2 + t1 + ylab("Prior probability") 

ggsave("meanPs.png", width=16, height=6)

#########################################################
m$which <- factor(m$which)
m$variable <- factor(m$variable)

stat_sum_df <- function(fun, geom="violin", ...) {
  stat_summary(fun.data = fun,
   geom = geom, width = 0.2, ...)
}

m.3 <- m %>%
		filter(!grepl("INT", variable)) %>%
		mutate(variable=gsub("TERM_","", variable)) %>%
		mutate(variable=gsub("0", "O", 
				variable)) %>%
		mutate(variable=gsub("1", "B", 
				variable)) %>%

		mutate(variable=substr(variable, 1,9))


head(m.3)

plt.3 <- ggplot(data=m.3, aes(x=variable, 
				y=value, color=which)) +
		#geom_point(aes(color=which), alpha=0.2) +
		#stat_summary(fun.data="mean_cl_boot",
			#geom="crossbar",
			# aes(color=which), size=1.5) +
		geom_violin(aes(color=which)) + #+
		#facet_wrap(~variable) + 
		#t1
	#stat_sum_df("mean_cl_boot",
	 #mapping = aes(group = which, color=which)) +
		#stat_summary(fun.y=mean, 
			#geom="point", shape=23, size=5) +
		#stat_summary(fun.data="mean_cl_boot",
			#aes(color=which), size=2 ) +

		t1

			#geom_violin(aes(group=which, color=which)) #,


ggsave("violin_mcmc.png", width=20, height=15)