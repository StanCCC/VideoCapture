@echo off & title

ffmpeg -formats 

cd /d %~dp0
 
for %%a in (*.*) do (
 
 ffmpeg -i "%%~sa" -y -f mp4 -filter:v scale=360:-1 "convert--%%~na.mp4"
 
)
 
pause


.echo  ffmpeg -i "%%~sa" -y -f mp4 -codec copy -q:v 1 "%%~na.mp4"