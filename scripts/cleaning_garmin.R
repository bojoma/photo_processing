library(tidyverse)

# --- Configuration ---
filename <- ".csv" #insert csv exported from garmin
survey_date <- "2026-" #insert month and day (mm-dd)
bay <- "" #insert bay code
camera <- "" #insert camera

# --- 1. Read the file as raw text ---
raw_lines <- readLines(filename, warn = FALSE)

# --- 2. Isolate the 'wpt' (Waypoint/Photo) section ---
header_idx <- which(str_detect(raw_lines, "^ID,lat,lon,ele,time"))[1]
data_indices <- which(str_detect(raw_lines, "^\\d+,"))
data_indices <- data_indices[data_indices > header_idx]

if (length(data_indices) > 0) {
  gaps <- which(diff(data_indices) > 1)
  if (length(gaps) > 0) {
    last_data_idx <- data_indices[gaps[1]] - 1
  } else {
    last_data_idx <- data_indices[length(data_indices)]
  }
  extract_lines <- c(raw_lines[header_idx], raw_lines[data_indices[1]:last_data_idx])
} else {
  stop("Could not find photo data in the wpt section.")
}

# --- 3. Parse the isolated text into a dataframe ---
garmin_wpt <- read.csv(text = extract_lines, header = TRUE, stringsAsFactors = FALSE, fill = TRUE)

# --- 4. Filter for photos and transform ---
coral_data <- garmin_wpt %>%
  filter(str_to_lower(type) == "photo") %>%
  mutate(
    Date = ymd_hms(time, quiet = TRUE) %>% as_date(),
    Date = if_else(is.na(Date), as_date(time), Date)
  ) %>%
  transmute(
    Filename = substr(as.character(name), 1, 8), #keeps only first 8 characters
    Camera = camera,
    Date = as.Date(survey_date),
    Bay = bay,
    `Coral location` = NA_character_, #insert coral location code if all same (e.g. "B")
    Lat = as.numeric(lat),
    Lon = as.numeric(lon),
    Species = NA_character_,
    Count = NA_real_,
    `Classified by` = NA_character_,
    `Length (cm)` = NA_real_,
    `Width (cm)` = NA_real_,
    `Area (cm2)` = NA_real_,
    `Measured by` = NA_character_,
    Link = NA_character_          
  )

# --- 5. Write to CSV ---
write.csv(coral_data, filename, row.names = FALSE, na = "")