# -*- coding: GBK -*-
import time
import re
import os
import subprocess

countdown = 0

class FFmpegServer():

    def __init__(self, log, append_log_row, btn_status):
        self.appendlog = log
        self.appendlog_row = append_log_row
        self.log_name = 'ffmpeg-gui-tool.log'
        self.modify_btn_status = btn_status

    def execute_ffmpeg(self, input_file, output_path, resolution, video_bitrate, audio_sampling_rate, audio_bitrate):
        file_dir = self.get_file_name(os.path.basename(input_file))
        if not os.path.exists(output_path + '/' + file_dir):
            os.mkdir(output_path + '/' + file_dir)
        output_path = os.path.abspath(output_path)
        ffmpeg_command = [
            'ffmpeg.exe',
            '-i', input_file,
            '-s', resolution,
            '-y',
            '-max_muxing_queue_size', '9999',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-pix_fmt', 'yuv420p',
            '-profile:v', 'high',
            '-level', '4.1',
            '-x264-params',
            'force-cfr=1:nal-hrd=vbr:bitrate={}:vbv-maxrate={}:vbv-bufsize={}:ref=3:keyint=50:bframes=3:fps=25'.format(
                video_bitrate, video_bitrate, video_bitrate),
            '-c:a', 'aac',
            '-ar', str(audio_sampling_rate),
            '-b:a', str(audio_bitrate) + 'k',
            '-ac', '2',
            '-hls_time', '10',
            '-hls_list_size', '10000',
            '-hls_segment_filename', '{}/{}/{}-%05d.ts'.format(output_path, file_dir, os.path.basename(input_file)),
            '-f', 'hls',
            '{}/{}/{}.m3u8'.format(output_path, file_dir, os.path.basename(input_file))
        ]
        open_ffmpeg_log = False
        if open_ffmpeg_log:
            with open(self.log_name, 'w') as log:
                process = subprocess.Popen(ffmpeg_command, shell=True,stdout=log, stderr=log)
            log.close()
        else:
            process = subprocess.Popen(ffmpeg_command, shell=True)
        return process

    # 获取单个文件切片进度
    def get_slice_progress(self, input_file, output_path):
        file_list = self.get_file_list(output_path + '/' + self.get_file_name(os.path.basename(input_file)))
        slice_file_count = len(file_list)
        return f'{slice_file_count - 1} slice files have been generated'

    # todo 获取批量文件处理进度 这里应该是程序入口，处理完成一个文件需要进行提示
    def file_progress(self, file_path, output_path, resolution, video_bitrate, audio_sampling_rate, audio_bitrate):
        global countdown
        countdown = 0
        file_list = []
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        if os.path.isdir(file_path):
            file_list = self.get_file_list(file_path)
        else:
            file_list.append(file_path)
        total_files = len(file_list)
        self.appendlog(f'Start processing {total_files} files ! ')
        err_files = []
        for file in file_list:
            self.get_exec_result(audio_bitrate, audio_sampling_rate, err_files, file, output_path,
                                 resolution, total_files, video_bitrate)
        if err_files:
            # todo 这里处理异常文件情况 删除文件列表 重新生成
            pass
        self.modify_btn_status(False)

    def get_exec_result(self, audio_bitrate, audio_sampling_rate, err_files, file, output_path, resolution,
                        total_files, video_bitrate):
        try:
            self.appendlog(f'start processing >>>>>>>> {file} ')
            # todo  这里应该是处理程序开始
            start = time.time()
            process = self.execute_ffmpeg(os.path.abspath(file), output_path, resolution, video_bitrate, audio_sampling_rate,
                                audio_bitrate)
            self.check_process_status(file, output_path, process, start, total_files)
        except Exception as e:
            self.appendlog(f'[ERROR] {file} 文件切片异常，已加入重试队列\t [{str(e)}]')
            err_files.append(file)
            self.modify_btn_status(False)

    def check_process_status(self, file, output_path, process, start, total_files):
        global countdown
        self.appendlog_row(f'正在转换文件 > {file} [')
        while True:
            self.appendlog_row('=')
            # 检查子进程是否已经结束
            if process.poll() is not None:
                # 子进程已经结束
                end = time.time()
                # todo  这里应该是处理程序结束
                countdown += 1
                processed_percent = (countdown / total_files) * 100
                # todo 更新处理进度
                self.appendlog_row(f']')
                self.appendlog(self.get_slice_progress(file, output_path) + f'\tused {(end - start):.2f} seconds')
                self.appendlog(f"Processed {countdown} out of {total_files} files ({processed_percent:.2f}%).")
                self.appendlog(f'文件输出路径：\t [{output_path + os.path.sep +  self.get_file_name(os.path.basename(file))}]')
                break
            time.sleep(2)


    # 获取系统文件列表
    def get_file_list(self, directory):
        files = []
        try:
            for filename in os.listdir(directory):
                # 获取文件的绝对路径
                file_path = os.path.abspath(os.path.join(directory, filename))
                # 如果是文件，则将其添加到列表中
                if os.path.isfile(file_path):
                    files.append(file_path)
            return files
        except Exception as e:
            self.appendlog(f'[ERROR] getting file list\t [{str(e)}]')
            return []

    def get_file_name(self, file):
        pattern = re.match('(.*?)\\.(.*)$', file)
        return pattern.group(1)

    # todo 这几个参数进行可选操作，文件和路径从页面进行输入
    # input_file = '测试.ts'  # 可能是一个路径，也可能是一个文件
    # output_path = './output'
    # resolution = '1280x720'
    # video_bitrate = '2000k'
    # audio_sampling_rate = 44100
    # audio_bitrate = 128
    # file_progress(input_file, output_path, resolution, video_bitrate, audio_sampling_rate, audio_bitrate)
