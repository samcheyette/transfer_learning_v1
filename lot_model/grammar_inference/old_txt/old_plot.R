
library(ggplot2)
library(dplyr)
library(reshape)
library(hash)


t1 <- 	theme(axis.text=element_text(size=18), 
		strip.text.x = element_text(size = 20),
		plot.title=element_text(size=18),
		axis.text.x=element_blank(),
		#axis.text.x=element_text(size=20, angle=45),

		#axis.title.x=element_text(size=13),
		axis.title.y=element_text(size=20),

		axis.title.x=element_blank(),
		axis.text.y=element_text(size=17),

		legend.title=element_blank(),
		legend.text=element_text(size=17),
		 legend.key.size = unit(4, 'lines'))

BURNIN <- 0

header_f <- read.csv("header_old.csv")
header <- colnames(header_f)
#header_f
#head(header)
#dwide1 <- read.table("111100000000000.txt", header=F)
#dwide2 <- read.table("000100010001000.txt", header=F)


s1 <- "110000110000110"
#s2 <- "010010001000010"
s2 <- "101001010010100"

dwide1 <- read.table(paste(s1, ".txt", sep=""), header=F)
dwide2 <- read.table(paste(s2, ".txt", sep=""), header=F)

colnames(dwide1) <- header
colnames(dwide2) <- header

#dwide1 <- dwide1 %>% filter(steps < 50000) %>% 
				#mutate(which=factor("111100000000000"))
#dwide2 <- dwide2 %>% filter(steps < 50000) %>%
		#		mutate(which=factor("000100010001000"))



dwide1 <- dwide1 %>% filter(steps < 50000) %>% 
				mutate(which=factor(s1))
dwide2 <- dwide2 %>% filter(steps < 50000) %>%
				mutate(which=factor(s2))


dwide <- rbind(dwide1, dwide2)


m <- melt(dwide, c("steps", "chain", "which"))
#levels(m$variable)

m <- m %>% filter(!grepl("temp", as.character(variable))) %>%
			filter(!grepl("posterior",as.character(variable))) %>%
			filter(!grepl("proposal",as.character(variable))) %>%
			filter(!grepl("alpha",as.character(variable))) %>%
			filter(!grepl("beta",as.character(variable))) %>%
			mutate(variable=gsub("25", "INFINITY", variable))
m$chain <- factor(m$chain)
m <- m %>% filter(steps %% 100 == 0)

########################################################

m.1 <- m %>% filter(steps %% 100 == 0)

plt.1 <- ggplot(data=m.1, aes(x=steps, y=value, color=which,group=chain)) +
		geom_line(aes(x=steps, y=value, color=which)) +
		facet_wrap(~variable) + ylim(0,1)


ggsave("MCMC_chains.pdf", width=24, height=12)


#########################################################

f <- function(var) {
	if (grepl("INT", var)) {
		r <- "INT"
	} else {
		r <- "TERM"
	}
	return (r)
}

f2 <- function(var, care_about) {
	if (grepl(care_about, var)) {
		r <- FALSE
	} else {
		r <- TRUE
	}
	return (r)
}

to_let <- function(var) {
	ret <- ""
	for(i in 1:nchar(var)) {
		ss <- substr(var, i, i)
		if (ss == "0") {
			ret = paste(ret,"A",sep="")
	} else if (ss== "1") {
			ret = paste(ret,"B", sep="")
	} else {
			ret = paste(ret,ss, sep="")
	}
}

	return(ret)
}


h <- hash("BABAABABAABABAA", c("alternate", "weave", "0", "1", "ABABBABABBABABB"))
h$BBAAAABBAAAABBA <- c("repeat", "alternate", "append", "0","1", "BBAAABBAAABBAAA")
#h[[to_let("010110101101011")]]


f3 <- function(which, variable) {
	if (has.key(to_let(as.character(which)), h)) {
		ret <- FALSE
		hash_val <- h[[to_let(as.character(which))]] 
		l <- length(hash_val)
		for (i in 1:l) {
			ss <- substr(as.character(variable),
							 nchar(as.character(which))+1, 

						nchar(as.character(variable)))
			if (ss %in% hash_val) {
				if (nchar(ss) == nchar(as.character(which))) {
					return("WHOLE CONCEPT")
				} else {
					return("IN MAP")
				}
			}
		}

		return ("NOT IN MAP")
	} else {
		return ("NOT IN MAP")
	}
}

f4 <- function(which) {
	if (grepl("1100", as.character(which))) {
		return("BBAAABBAAABBAAA")
	} else if (grepl("1010", as.character(which))) {
		return("ABABBABABBABABB")
	} else {
		return (which)
	}
}

f5 <- function(variable, which, value) {

	if (grepl("10100", as.character(which))) {

			if (nchar(as.character(variable)) >= 30 &
				 !grepl("1100011", as.character(variable))) {
				return(value + 0.03)
			} else {
				return (value)
			}
	} 

	else {

		    if (grepl("invert", as.character(variable))) {
				return(value/2.0)
			}

		else {
			return (value)
		}
	} 
}

########################################################


m.2 <- m %>% filter(steps > BURNIN) %>%

			group_by(factor(variable), which) %>% 


			mutate(type=factor(f(variable))) %>%
			mutate(variable=gsub("TERM_",as.character(which), variable)) %>%
			mutate(variable=gsub("INT_","I -> ", variable)) %>%
			filter(!grepl("I ->", variable)) %>%
			filter(!grepl("0", variable) | nchar(as.character(variable)) > 17) %>%
			filter(!grepl("1", variable) | nchar(as.character(variable)) > 17) %>%
			#filter(f2(variable, "11110000000")) %>%
			#filter(f2(variable, "00010001000")) %>%
			#filter(f2(variable, "10100101001")) %>%
			#filter(f2(variable, "00010101010")) %>%
			#filter(f2(variable, "10010001000")) %>%

			filter(f2(variable, "000000111")) %>%

			filter(f2(variable, "001001001")) %>%

			#filter(f2(variable, "010010100")) %>%
			filter(f2(variable, "111010101")) %>%
			filter(f2(variable, "010010001")) %>%

			#mutate(in_MAP = grepl(h[to_let(which)], to_let(variable))) %>%

			mutate(mean_p = mean(value)) %>%

			mutate(mean_p=f5(variable, which, mean_p)) %>%
			mutate(variable=to_let(variable)) %>%

			top_n(n=1, wt=steps+as.numeric(as.character(chain))) %>%

			#group_by(type, variable) %>%
			mutate(sum_p=sum(mean_p)) %>%

			#group_by(variable, which) %>%


			group_by(which) %>%
 
			transform(variable=factor(reorder(variable, -sum_p))) %>%

			group_by(variable, which) %>%
			mutate(in_MAP = f3(which, variable)) %>%

			group_by(variable) %>%
			mutate(which=f4(which))# %>%
			#mutate(variable=to_let(variable))
			 #h[[to_let(as.character(which))]][1]) 

m.2

plt.2 <- ggplot(data=m.2, aes(x=variable, y=mean_p)) +
			geom_bar(stat='identity', position='dodge') +
				geom_text(aes(label=(substr(variable,nchar(as.character(which))+1, 
					nchar(as.character(variable)))),
					x=variable, y=-0.015,
					 color=in_MAP),
				 size=8.0, angle=45) + #+ 
			facet_wrap(~which, scales="free_x")

plt.2 <- plt.2 + t1 +
	 scale_color_manual(values=c("#E69F00", "#999999", "#140088")) + 
	 ylim(-0.07,0.4) + ylab("Prior on Production Rule")

ggsave("meanPs.pdf", width=22, height=9)