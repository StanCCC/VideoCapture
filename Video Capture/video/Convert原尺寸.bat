@echo off & title
 
cd /d %~dp0
 
for %%a in (*.*) do (
 
 ffmpeg -i "%%~sa" -y -f mp4 -codec copy -q:v 1 "%%~na.mp4"
 
)
 
pause