library(readxl)
library(ggplot2)
library(reshape2) 
library(plyr)
library(dplyr)
library(ggthemes) # Charger
library(tidyverse)




#Execute the whole script to print figure 2, 3 and 4 from the article.


# Uncertainty 



#Load data

Aalborg_NoThermonight <- read_excel("results_table_df_Aal_Nothermo.xlsx")
Aalborg_Thermonight <- read_excel("results_table_df_Aal_thermo.xlsx")

#Adding column Thermoregulation at night

Aalborg_NoThermonight$`Thermoregulation at night`<-'No'
Aalborg_Thermonight$`Thermoregulation at night`<-'Yes'

Aalborg_total <- rbind(Aalborg_NoThermonight, Aalborg_Thermonight)
Aalborg_total$`Thermoregulation at night`<-as.factor(Aalborg_total$`Thermoregulation at night`)

#Adding column Location

Aalborg_total$Location='Aalborg'
Aalborg_total$Location<-as.factor(Aalborg_total$Location)


# Granada

Granada_NoThermonight=read_excel('results_table_df_Gra_Nothermo.xlsx')
Granada_Thermonight=read_excel('results_table_df_Gra_thermo.xlsx')

#Adding column Thermoregulation at night

Granada_NoThermonight$`Thermoregulation at night`<-'No'
Granada_Thermonight$`Thermoregulation at night`<-'Yes'

Granada_total <- rbind(Granada_NoThermonight, Granada_Thermonight)
Granada_total$`Thermoregulation at night`<-as.factor(Granada_total$`Thermoregulation at night`)

#Adding column Location
Granada_total$Location='Granada'
Granada_total$Location<-as.factor(Granada_total$Location)


#Combining the two locations

Total=rbind(Aalborg_total,Granada_total)


# Modify names IC to include unit



names(Total)[names(Total) == "WDP"] <- "WDP, m3 water"
names(Total)[names(Total) == "GWP100"] <- "GWP100, kg CO2-eq"
names(Total)[names(Total) == "FEP"] <- "FEP, kg P-eq"
names(Total)[names(Total) == "TETPinf"] <- "TETPinf, kg 1.4-DC"


#Melt 

Total_melted=melt(Total,measure.vars = c("WDP, m3 water","GWP100, kg CO2-eq","FEP, kg P-eq","TETPinf, kg 1.4-DC"),variable.name = 'Impact_Category',value.name='Score')

Total_melted$Impact_Category=as.factor(Total_melted$Impact_Category)

# To label IC with exponents and subscripts, we create a new column 
# identical to IC but with an expression

Total_melted$facets = factor(Total_melted$Impact_Category, labels = c(
  "WDP ~(m^{3}~water)", 
  "GWP100~(kg~CO[2]-eq)", 
  "FEP~(kg~P-eq)",
  "TETPinf~(kg~1.4-DC)"))

# Add mean column for plot vercital lines

Total_melted <- Total_melted %>% group_by(facets,`Thermoregulation at night`,Location)%>% 
  mutate(mean = mean(Score),median=median(Score)) %>% # calculate mean for plotting as well
  ungroup()


p=ggplot(Total_melted, aes(x=Score,fill=`Thermoregulation at night`,..scaled..))
p=p+geom_vline(aes(xintercept = mean,col=`Thermoregulation at night`), linetype = "longdash")
p=p+geom_density(alpha=0.7,color=NA,)+theme_bw()
p=p+facet_grid(Location ~ facets,scales='free',labeller = label_parsed)
p=p+theme(strip.text.x = element_text(size = 12, colour = "black",angle=0))
p=p+theme(strip.text.y = element_text(size = 12, colour = "black", angle = -90))
p=p+theme(legend.position="bottom")
p=p+theme(legend.title = element_text(size=12))+theme(legend.text = element_text(size=2)) #change legend text font size
p=p+theme(legend.key.size = unit(0.2, 'cm'), #change legend key size
          legend.key.height = unit(0.2, 'cm'), #change legend key height
          legend.key.width = unit(0.2, 'cm'),
          legend.text = element_text(size=10)) #change legend text font size
p
ggsave('Figure_uncertainty.jpeg', width = 10, height = 7,dpi=600)










# Sensitivity


# Load Data and add columns with  categorical variables for location and thermoregulation

sensimulti_Gra_Nothermo <- read_excel("sensi_multi_melt_Gra_Nothermo.xlsx")
sensimulti_Gra_thermo <- read_excel("sensi_multi_melt_Gra_thermo.xlsx")


sensimulti_Gra_Nothermo$location='Granada'
sensimulti_Gra_thermo$location='Granada'


sensimulti_Aal_Nothermo <- read_excel("sensi_multi_melt_Aal_Nothermo.xlsx")
sensimulti_Aal_thermo <- read_excel("sensi_multi_melt_Aal_thermo.xlsx")

sensimulti_Aal_thermo$location='Aalborg'
sensimulti_Aal_Nothermo$location='Aalborg'

# Add column Thermo
sensimulti_Aal_Nothermo$`Thermoregulation at night`='No'
sensimulti_Gra_Nothermo$`Thermoregulation at night`='No'

sensimulti_Gra_thermo$`Thermoregulation at night`='Yes'
sensimulti_Aal_thermo$`Thermoregulation at night`='Yes'


# Change names to variance

names(sensimulti_Gra_thermo)[names(sensimulti_Gra_thermo) == "value"] <- "% variance"
names(sensimulti_Gra_Nothermo)[names(sensimulti_Gra_Nothermo) == "value"] <- "% variance"
names(sensimulti_Aal_Nothermo)[names(sensimulti_Aal_Nothermo) == "value"] <- "% variance"
names(sensimulti_Aal_thermo)[names(sensimulti_Aal_thermo) == "value"] <- "% variance"

Sensi_total=rbind(sensimulti_Aal_Nothermo,
                  sensimulti_Gra_Nothermo,
                  sensimulti_Gra_thermo,
                  sensimulti_Aal_thermo)

Sensi_total$`Thermoregulation at night`<-as.factor(Sensi_total$`Thermoregulation at night`)
Sensi_total$location<-as.factor(Sensi_total$location)



# SELECT IMPACT CATEGORIES

sensimulti_Gra_thermo <- subset(sensimulti_Gra_thermo , Impact_Category == 'GWP100' | Impact_Category == 'FEP'| Impact_Category == 'WDP'| Impact_Category == 'TETPinf')
Sensi_total<- subset(Sensi_total , Impact_Category == 'GWP100' | Impact_Category == 'FEP'| Impact_Category == 'WDP'| Impact_Category == 'TETPinf')


# Changes names column "Value
names(sensimulti_Gra_thermo)[names(sensimulti_Gra_thermo) == "value"] <- "% variance"
names(sensimulti_Gra_thermo)[names(sensimulti_Gra_thermo) == "Impact_Category"] <- "Impact Category"

names(Sensi_total)[names(Sensi_total) == "Impact_Category"] <- "Impact Category"
names(Sensi_total)[names(Sensi_total) == "% variance"] <- "% Total-order Sensitivity"



#OK

ggplot(sensimulti_Gra_thermo, aes(fill=Parameter, y=`% variance`, x=Impact_Category)) + 
  geom_bar(position="fill", stat="identity")+ scale_fill_brewer(palette="Dark1")


(ggplot(Sensi_total, aes(fill=Parameter, y=`% Total-order Sensitivity`, x=`Impact Category`))
  + geom_bar(position="fill", stat="identity")
  +facet_grid(vars(location))
  +theme_bw()
    
  +scale_fill_brewer(palette="Spectral")
  +theme(legend.title = element_text(size=10))
  +theme(legend.text = element_text(size=9)) 
 )
ggsave('Figure_sensitivity.jpeg', width = 5, height = 5,dpi=600)












#####  Contribution

# Geom split violion functions for plot


GeomSplitViolin <- ggproto("GeomSplitViolin", GeomViolin, 
                           draw_group = function(self, data, ..., draw_quantiles = NULL) {
                             data <- transform(data, xminv = x - violinwidth * (x - xmin), xmaxv = x + violinwidth * (xmax - x))
                             grp <- data[1, "group"]
                             newdata <- plyr::arrange(transform(data, x = if (grp %% 2 == 1) xminv else xmaxv), if (grp %% 2 == 1) y else -y)
                             newdata <- rbind(newdata[1, ], newdata, newdata[nrow(newdata), ], newdata[1, ])
                             newdata[c(1, nrow(newdata) - 1, nrow(newdata)), "x"] <- round(newdata[1, "x"])
                             
                             if (length(draw_quantiles) > 0 & !scales::zero_range(range(data$y))) {
                               stopifnot(all(draw_quantiles >= 0), all(draw_quantiles <=
                                                                         1))
                               quantiles <- ggplot2:::create_quantile_segment_frame(data, draw_quantiles)
                               aesthetics <- data[rep(1, nrow(quantiles)), setdiff(names(data), c("x", "y")), drop = FALSE]
                               aesthetics$alpha <- rep(1, nrow(quantiles))
                               both <- cbind(quantiles, aesthetics)
                               quantile_grob <- GeomPath$draw_panel(both, ...)
                               ggplot2:::ggname("geom_split_violin", grid::grobTree(GeomPolygon$draw_panel(newdata, ...), quantile_grob))
                             }
                             else {
                               ggplot2:::ggname("geom_split_violin", GeomPolygon$draw_panel(newdata, ...))
                             }
                           })

geom_split_violin <- function(mapping = NULL, data = NULL, stat = "ydensity", position = "identity", ..., 
                              draw_quantiles = NULL, trim = TRUE, scale = "area", na.rm = FALSE, 
                              show.legend = NA, inherit.aes = TRUE) {
  layer(data = data, mapping = mapping, stat = stat, geom = GeomSplitViolin, 
        position = position, show.legend = show.legend, inherit.aes = inherit.aes, 
        params = list(trim = trim, scale = scale, draw_quantiles = draw_quantiles, na.rm = na.rm, ...))
}





# New version with quantiles indication in the areas


GeomSplitViolin <- ggproto("GeomSplitViolin", GeomViolin,
                           draw_group = function(self, data, ..., draw_quantiles = NULL) {
                             # Original function by Jan Gleixner (@jan-glx)
                             # Adjustments by Wouter van der Bijl (@Axeman)
                             data <- transform(data, xminv = x - violinwidth * (x - xmin), xmaxv = x + violinwidth * (xmax - x))
                             grp <- data[1, "group"]
                             newdata <- plyr::arrange(transform(data, x = if (grp %% 2 == 1) xminv else xmaxv), if (grp %% 2 == 1) y else -y)
                             newdata <- rbind(newdata[1, ], newdata, newdata[nrow(newdata), ], newdata[1, ])
                             newdata[c(1, nrow(newdata) - 1, nrow(newdata)), "x"] <- round(newdata[1, "x"])
                             if (length(draw_quantiles) > 0 & !scales::zero_range(range(data$y))) {
                               stopifnot(all(draw_quantiles >= 0), all(draw_quantiles <= 1))
                               quantiles <- create_quantile_segment_frame(data, draw_quantiles, split = TRUE, grp = grp)
                               aesthetics <- data[rep(1, nrow(quantiles)), setdiff(names(data), c("x", "y")), drop = FALSE]
                               aesthetics$alpha <- rep(1, nrow(quantiles))
                               both <- cbind(quantiles, aesthetics)
                               quantile_grob <- GeomPath$draw_panel(both, ...)
                               ggplot2:::ggname("geom_split_violin", grid::grobTree(GeomPolygon$draw_panel(newdata, ...), quantile_grob))
                             }
                             else {
                               ggplot2:::ggname("geom_split_violin", GeomPolygon$draw_panel(newdata, ...))
                             }
                           }
)

create_quantile_segment_frame <- function(data, draw_quantiles, split = FALSE, grp = NULL) {
  dens <- cumsum(data$density) / sum(data$density)
  ecdf <- stats::approxfun(dens, data$y)
  ys <- ecdf(draw_quantiles)
  violin.xminvs <- (stats::approxfun(data$y, data$xminv))(ys)
  violin.xmaxvs <- (stats::approxfun(data$y, data$xmaxv))(ys)
  violin.xs <- (stats::approxfun(data$y, data$x))(ys)
  if (grp %% 2 == 0) {
    data.frame(
      x = ggplot2:::interleave(violin.xs, violin.xmaxvs),
      y = rep(ys, each = 2), group = rep(ys, each = 2)
    )
  } else {
    data.frame(
      x = ggplot2:::interleave(violin.xminvs, violin.xs),
      y = rep(ys, each = 2), group = rep(ys, each = 2)
    )
  }
}

geom_split_violin <- function(mapping = NULL, data = NULL, stat = "ydensity", position = "identity", ..., 
                              draw_quantiles = NULL, trim = TRUE, scale = "area", na.rm = FALSE, 
                              show.legend = NA, inherit.aes = TRUE) {
  layer(data = data, mapping = mapping, stat = stat, geom = GeomSplitViolin, position = position, 
        show.legend = show.legend, inherit.aes = inherit.aes, 
        params = list(trim = trim, scale = scale, draw_quantiles = draw_quantiles, na.rm = na.rm, ...))
}









# Load data
contrib_Aal_thermo <- read.csv(file="all_methods_contribution_df_melted_Aal_thermo.csv",sep=';',header=FALSE)
contrib_Aal_Nothermo <- read.csv(file="all_methods_contribution_df_melted_Aal_Nothermo.csv",sep=';',header=FALSE)
contrib_Gra_Nothermo <- read.csv(file="all_methods_contribution_df_melted_Gra_Nothermo.csv",sep=';',header=FALSE)
contrib_Gra_thermo <- read.csv(file="all_methods_contribution_df_melted_Gra_thermo.csv",sep=';',header=FALSE)

names(contrib_Aal_thermo) <- contrib_Aal_thermo[1,]
contrib_Aal_thermo <- contrib_Aal_thermo[-1,]

names(contrib_Aal_Nothermo) <- contrib_Aal_Nothermo[1,]
contrib_Aal_Nothermo <- contrib_Aal_Nothermo[-1,]

names(contrib_Gra_Nothermo) <- contrib_Gra_Nothermo[1,]
contrib_Gra_Nothermo <- contrib_Gra_Nothermo[-1,]

names(contrib_Gra_thermo) <- contrib_Gra_thermo[1,]
contrib_Gra_thermo <- contrib_Gra_thermo[-1,]


# Add categorical columns to the dataframes
contrib_Aal_thermo$Location<-'Aalborg'
contrib_Aal_Nothermo$Location<-'Aalborg'
contrib_Gra_thermo$Location<-'Granada'
contrib_Gra_Nothermo$Location<-'Granada'



contrib_Aal_thermo$`Thermoregulation at night`<-'Yes'
contrib_Aal_Nothermo$`Thermoregulation at night`<-'No'
contrib_Gra_thermo$`Thermoregulation at night`<-'Yes'
contrib_Gra_Nothermo$`Thermoregulation at night`<-'No'



# Combine in 1 dataframe
contribtot <- rbind(contrib_Aal_thermo,
                    contrib_Aal_Nothermo,
                    contrib_Gra_thermo,
                    contrib_Gra_Nothermo)
contribtot$Location<-as.factor(contribtot$Location)
contribtot$`Thermoregulation at night`<-as.factor(contribtot$`Thermoregulation at night`)
contribtot$`% of total impact`<-as.numeric(contribtot$`% of total impact`)


# Choose only 4 Impact categories

contribtot<- subset(contribtot , `Impact Category` == 'GWP100' | `Impact Category` == 'FEP'| `Impact Category` == 'WDP'| `Impact Category` == 'TETPinf')

# Keep only processes that contributed significantly


processes_to_keep = c("Thermoregulation",
                      "Harvesting",
                      "Post harvest processing",
                      "Nutrients consumption",
                      "Culture mixing",
                      "Substitution by co-products",
                      "CO2 consumption",
                      "Cleaning") 
                      
                      
contribtot=contribtot[contribtot$Processes %in% processes_to_keep,]

contribtot %>%
  mutate(class = fct_reorder(Processes, `% of total impact`, .fun='median')) %>%
  ggplot( aes(x=reorder(Processes, `% of total impact`), y=`% of total impact`, fill=Location)) + 
  geom_split_violin(adjust=1,scale='width',trim=T,draw_quantiles = c( 0.5),alpha=0.4)+
  scale_fill_manual(values=c("Orange", "Green"))+
  theme_bw()+
  facet_grid(vars(`Impact Category`),scales='free')+
  theme(axis.text.x = element_text( size=12, color='black', angle=90),
        axis.text.y = element_text( size=12,color='black',angle=0),
        axis.title=element_text(size=14,color='black',face="bold"),
        legend.key.size = unit(0.3, 'cm'),
        legend.key.height = unit(0.3, 'cm'),
        legend.key.width = unit(0.3, 'cm'),
        legend.text = element_text(size=14),
        strip.text.y = element_text(size = 18))+
  xlab("Processes (modules)")

ggsave('Figure_contributions.jpeg', width = 10, height = 10,dpi=600)







