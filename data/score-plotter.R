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

histogram_wc <- data |>
  ggplot(aes(x = words)) +
  theme_minimal() +
  geom_histogram(binwidth = 5, fill = '#14a88e') +
  labs(
    x = 'Number of Words',
    y = 'Game Count'
  )

cumulative_sum_wc <- data |>
  ggplot(aes(x = words)) +
  theme_minimal() +
  stat_bin(aes(y = cumsum(..count..)), geom = 'step', binwidth = 5) +
  scale_y_continuous(
    sec.axis = sec_axis(trans = ~ . / 365, name = 'Years of games at or below threshold')
  ) +
  labs(
    x = 'Word threshold',
    y = 'Number of games at or below threshold'
  )

library(patchwork)

(histogram + histogram_wc) / (cumulative_sum + cumulative_sum_wc)
ggsave('all_scores.png', width = 6, height = 6)

data |>
  ggplot(aes(x = score, y = words)) +
  theme_minimal() +
  geom_bin_2d() +
  scale_fill_viridis_c() +
  labs(
    x = 'Total Score',
    y = 'Number of Words',
    fill = 'Number of\nGames'
  )
ggsave('words-v-games.png', width = 4, height = 4, bg = 'white')

data |>
  group_by(required) |>
  mutate(binned = cut(score, seq(0,500,10))) |>
  count(binned) |>
  pivot_wider(names_from = required, values_from = n) |>
  mutate(across(a:z, ~replace_na(.x, 0))) |>
  mutate(total = (a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q + r + t + u + v + w + x + y + z)/10) |>
  pivot_longer(cols = a:z, names_to = 'required', values_to = 'count') |>
  mutate(binned = as.numeric(binned) * 10) |>
  ggplot(aes(x = binned)) +
  geom_step(aes(y = total)) +
  geom_col(aes(y = count, fill = required)) +
  scale_x_continuous(breaks = seq(0,500,250)) +
  theme_minimal() +
  facet_wrap(vars(required), nrow = 4, ncol = 7) +
  theme(legend.position = 'none')
ggsave('scores_by_req_letter.png', width = 10, height = 10, bg = 'white')


data |>
  group_by(letters) |>
  summarize(min_score = min(score)) |>
  right_join(data) |>
  group_by(required) |>
  summarize(additional = median(score - min_score)) |>
  mutate(required = fct_reorder(required, -additional)) |>
  ggplot(aes(x = required, y = additional)) +
  theme_minimal() +
  geom_col(fill = '#f9ad7e') +
  labs(
    x = 'Required letter',
    y = 'Median points-over-minimum'
  )
ggsave('points-over-minimum.png', width = 4, height = 4, bg = 'white')

data |>
  filter(score <= 250) |>
  write_csv('filtered_words.csv')
