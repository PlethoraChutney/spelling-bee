library(tidyverse)

data <- read_csv('../data/calculated_scores.csv') %>% 
  separate(words_score, into = c(NA, 'num_words', 'total_score', NA), convert = TRUE) %>% 
  pivot_longer(cols = c('good', 'Jump'), names_to = 'Metric', values_to = 'Value') %>% 
  pivot_longer(cols = c('num_words', 'total_score'), names_to = 'difficulty', values_to = 'diff_level') %>% 
  select(Metric, Value, difficulty, diff_level)

data %>% 
  ggplot(aes(x = diff_level, y = Value)) +
  theme_minimal() +
  geom_jitter(alpha = 0.5) +
  geom_smooth(formula = y~x, method = 'lm', se = FALSE, color = 'black') +
  facet_grid(rows = vars(Metric), cols = vars(difficulty), scales = 'free') +
  scale_y_continuous(breaks = seq(0, 16, 2))
