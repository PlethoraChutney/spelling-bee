library(tidyverse)

data <- read_csv('all_scores.csv')

histogram <- data |>
  ggplot(aes(x = score)) +
  theme_minimal() +
  geom_histogram(binwidth = 10, fill = '#14a88e') +
  coord_cartesian(xlim = c(0, 500)) +
  labs(
    x = 'Total Score',
    y = 'Game Count'
  )

cumulative_sum <- data |>
  ggplot(aes(x = score)) +
  theme_minimal() +
  stat_bin(aes(y = cumsum(..count..)), geom = 'step', binwidth = 10) +
  coord_cartesian(xlim = c(0, 500)) +
  scale_y_continuous(
    sec.axis = sec_axis(trans = ~ . / 365, name = 'Years of games at or below threshold')
  ) +
  labs(
    x = 'Score threshold',
    y = 'Number of games at or below threshold'
  )

library(patchwork)

histogram / cumulative_sum
ggsave('all_scores.png', width = 6, height = 6)