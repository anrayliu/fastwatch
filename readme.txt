Fastwatch is a program that's used with command line arguments.

List of arguments:

source         : type of video
target         : name of video
-s --season    : which season to play
-e --episode   : which episode to play
-d --dub       : open the dubbed version for anime

Example:

watch tv "breaking bad" -s 1 -e 1

The most recently watched episode for each show is tracked, so if no episode is specified,
the next episode will be played. Similarly, if source is "last", the next episode for the
most recently watched show will be played.

Note: Include the season into the title for anime (e.g. "attack on titan 2")
