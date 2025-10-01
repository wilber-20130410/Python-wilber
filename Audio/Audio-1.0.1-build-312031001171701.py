# -*- coding: utf-8 -*-
'''
名称:音频可视化
作者:wilber-20130410
版权: © 2025 wilber-20130410
版本:1.0.1[312031001171701](正式版)
日期:2025.10.1
留言:
1.使用者需要具有python3基础,并有以下所使用的各种库的基础。
2.使用前请阅读这段注释。
3.Linux(Ubuntu)系统需要确保jack服务的运行。
4.使用前请确保已经安装以下所使用的库。
5.本人推荐使用Visual Studio Code或PyCharm Community作为IDE(集成开发环境)。
6.需要安装python3及以上python环境(本人使用python3.12.3)。
7.本代码无法直接使用，请根据自身情况进行调整。
8.AudioVisualizer_output()模块的功能若无法使用为正常现象，本人也无力解决。
9.字体和背景音乐要放在工作目录中,即IDE所打开的目录,或命令行所在的目录。
10.关闭界面时,如果报错,属于正常现象。
11.代码存在某些Bug,可以自行修复,或向本人邮箱xuwb0410@163.com(github项目界面也可以)提交错误并等待更新。
12.如果您有建议、发现了Bug、问题或者您进行优化后的代码,欢迎向本人邮箱xuwb0410@163.com发送邮件,本人将在21天内进行回复。
13.以上留言不分先后。
'''
import pygame
import numpy as np
import random
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
from noise import pnoise2
from pygame import mixer
import threading
from tkinter import Tk, filedialog
import warnings
import math
import os
import pyaudio
import time
import sys
import requests
warnings.filterwarnings("ignore")
wifi = False

class AudioVisualizerLauncher:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.WIDTH, self.HEIGHT = 854, 480
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.NOFRAME)
        pygame.display.set_caption("AudioVisualizer 1.0.1[312031001171701]")
        self.BLACK = (0, 0, 0)
        self.DARK_GREEN = (0, 71, 0)
        self.GREEN = (0, 100, 0)
        self.LIGHT_GREEN = (100, 200, 100)
        self.WHITE = (255, 255, 255)
        self.GRAY = (100, 100, 100)
        self.LIGHT_GRAY = (200, 200, 200)
        self._load_fonts()
        self.background_layers = []
        self.layer_positions = [0, 0, 0]
        self._init_background()
        self.title_text = self.title_font.render("AudioVisualizer", True, self.WHITE)
        self.title_shadow = self.title_font.render("AudioVisualizer", True, self.GRAY)
        self.title_rect = self.title_text.get_rect(center=(self.WIDTH//2, self.HEIGHT//3))
        self.version_text = self.version_font.render("1.0.1[312031001171701]", True, self.LIGHT_GRAY)
        self.version_rect = self.version_text.get_rect(bottomright=(self.WIDTH-10, self.HEIGHT-10))
        self.progress_width = self.WIDTH - 100
        self.progress_height = 5
        self.progress_rect = pygame.Rect(
            (self.WIDTH - self.progress_width) // 2, 
            self.HEIGHT * 2 // 3, 
            self.progress_width, 
            self.progress_height
        )
        self.progress = 0
        self.loading_texts = [
            "Starting...",
            "Checking resource integrity...",
            "Checking colorer...",
            "Checking resource patches...",
            "Being logged in...",
            "Downloading data...",
            "Checking data integrity...",
            "Startup complete",
        ]
        self.current_loading_text = "Starting AudioVisualizer..."
        self.running = True
        self.clock = pygame.time.Clock()
        self.start_time = time.time()

    def game_stop(self):
        mixer.music.stop()
        self.current_loading_text = "Network anomaly , please check the network and restart"
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            self._draw()
            pygame.display.flip()
            self.clock.tick(60)

    def _load_fonts(self):
        """加载字体"""
        try:
            self.title_font = pygame.font.Font("Minecraft.ttf", 72)
            self.version_font = pygame.font.Font("Minecraft.ttf", 16)
            self.progress_font = pygame.font.Font("Minecraft.ttf", 14)
        except:
            self.title_font = pygame.font.SysFont("arial", 72, bold=True)
            self.version_font = pygame.font.SysFont("arial", 16)
            self.progress_font = pygame.font.SysFont("arial", 14)
    
    def _init_background(self):
        """初始化背景"""
        for i in range(3):
            layer = pygame.Surface((self.WIDTH, self.HEIGHT))
            for _ in range(100):
                x = random.randint(0, self.WIDTH)
                y = random.randint(0, self.HEIGHT)
                size = random.randint(1, 3) * (i + 1)
                color = (random.randint(0, 50), random.randint(50, 100), random.randint(0, 50))
                pygame.draw.rect(layer, color, (x, y, size, size))
            self.background_layers.append(layer)
    
    def _handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def _update_progress(self):
        """更新进度条"""
        if self.progress < 100:
            self.progress += random.uniform(0.05, 0.2)
            self.progress = min(self.progress, 100)
            self._update_loading_text()
    
    def _update_loading_text(self):
        """更新加载文本"""
        global wifi
        if self.progress < 5:
            self.current_loading_text = self.loading_texts[0]
        elif 5 <= self.progress < 15:
            if wifi:
                self.current_loading_text = self.loading_texts[1]
            else:
                self.current_loading_text = "Network anomaly , please check the network and restart"
        elif 15 <= self.progress < 25:
            if wifi:
                self.current_loading_text = self.loading_texts[2]
            else:
                self.game_stop()
        elif 25 <= self.progress < 35:
            self.current_loading_text = self.loading_texts[3]
        elif 35 <= self.progress < 60:
            self.current_loading_text = self.loading_texts[4]
        elif 60 <= self.progress < 80:
            self.current_loading_text = self.loading_texts[5]
        elif 80 <= self.progress < 90:
            self.current_loading_text = self.loading_texts[6]
        elif self.progress >= 90:
            self.current_loading_text = self.loading_texts[7]
    
    def _update_background(self):
        """更新背景位置"""
        for i in range(3):
            self.layer_positions[i] += (i + 1) * 0.2
            if self.layer_positions[i] > self.WIDTH:
                self.layer_positions[i] = 0
    
    def _draw_background(self):
        """绘制背景"""
        for i, layer in enumerate(self.background_layers):
            self.screen.blit(layer, (self.layer_positions[i] - self.WIDTH, 0))
            self.screen.blit(layer, (self.layer_positions[i], 0))
    
    def _draw_title(self):
        """绘制标题"""
        self.screen.blit(self.title_shadow, (self.title_rect.x + 3, self.title_rect.y + 3))
        self.screen.blit(self.title_text, self.title_rect)
    
    def _draw_progress_bar(self):
        """绘制进度条"""
        pygame.draw.rect(self.screen, self.GRAY, self.progress_rect)
        filled_rect = pygame.Rect(
            self.progress_rect.x, 
            self.progress_rect.y, 
            self.progress_rect.width * (self.progress / 100), 
            self.progress_rect.height
        )
        pygame.draw.rect(self.screen, self.GREEN, filled_rect)
        pygame.draw.rect(self.screen, self.LIGHT_GREEN, filled_rect, 1)
        loading_surface = self.progress_font.render(self.current_loading_text, True, self.LIGHT_GRAY)
        loading_rect = loading_surface.get_rect(midbottom=(self.WIDTH//2, self.progress_rect.y - 10))
        self.screen.blit(loading_surface, loading_rect)
        if self.progress >= 100:
            continue_text = self.progress_font.render("Loading Complete - Press any key", True, self.LIGHT_GREEN)
            continue_rect = continue_text.get_rect(midtop=(self.WIDTH//2, self.progress_rect.bottom + 20))
            self.screen.blit(continue_text, continue_rect)
    
    def _draw_version(self):
        """绘制版本信息"""
        self.screen.blit(self.version_text, self.version_rect)
    
    def _update(self):
        """更新状态"""
        self._update_background()
        self._update_progress()
    
    def _draw(self):
        """绘制"""
        self.screen.fill(self.DARK_GREEN)
        self._draw_background()
        self._draw_title()
        self._draw_progress_bar()
        self._draw_version()
        pygame.display.flip()
    
    def run_game(self):
        start = [1, 2, 3, 4, 5, 6]
        random.shuffle(start)
        stnum = random.choice(start)
        if stnum % 2 == 1:
            app = AudioVisualizer_start_2()
            app.run()
        else:
            app_1 = AudioVisualizer_start_1()
            app_1.run()

    def run(self):
        """运行游戏主循环"""
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(60)
            if self.progress >= 100:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        self.running = False
                        break
        self.run_game()
        pygame.quit()

class AudioVisualizer_start_1:
    """音频可视化主类"""
    
    class Particle:
        """粒子系统类"""
        def __init__(self, width, height):
            self.x = random.randint(0, width)
            self.y = random.randint(0, height)
            self.size = random.uniform(1, 3)
            self.speed = random.uniform(0.2, 1.5)
            self.color = (
                random.randint(70, 100),
                random.randint(120, 180),
                random.randint(200, 255),
                random.randint(150, 220)
            )
            self.direction = random.uniform(0, 2 * math.pi)
            self.width = width
            self.height = height
            
        def update(self):
            """更新粒子位置"""
            self.x += math.cos(self.direction) * self.speed
            self.y += math.sin(self.direction) * self.speed
            if self.x < 0 or self.x > self.width or self.y < 0 or self.y > self.height:
                self.reset()
                
        def reset(self):
            """重置粒子位置"""
            self.x = random.randint(0, self.width)
            self.y = random.randint(0, self.height)
            self.direction = random.uniform(0, 2 * math.pi)
        
        def draw(self, surface):
            """绘制粒子"""
            pygame.draw.circle(
                surface, 
                self.color, 
                (int(self.x), int(self.y)), 
                int(self.size)
            )
    
    class MindustryButton:
        """Mindustry风格按钮类"""
        def __init__(self, x, y, width, height, text, fonts, colors):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.state = 'normal'  # normal, hover, pressed
            self.animation = 0
            self.fonts = fonts
            self.colors = colors
            
        def update(self, mouse_pos, mouse_clicked):
            """更新按钮状态"""
            if self.rect.collidepoint(mouse_pos):
                if mouse_clicked:
                    self.state = 'pressed'
                else:
                    self.state = 'hover'
            else:
                self.state = 'normal'  
            if self.state == 'hover' and self.animation < 10:
                self.animation += 1
            elif self.state == 'pressed' and self.animation > -5:
                self.animation -= 1
            elif self.state == 'normal' and self.animation > 0:
                self.animation -= 1
                
        def draw(self, surface):
            """绘制按钮"""
            if self.state == 'pressed':
                color = self.colors['button_pressed']
            elif self.state == 'hover':
                color = self.colors['button_hover']
            else:
                color = self.colors['button']
            pygame.draw.rect(surface, color, self.rect, border_radius=3)
            highlight = pygame.Surface((self.rect.width, max(2, self.rect.height // 4)), pygame.SRCALPHA)
            highlight.fill((255, 255, 255, 30))
            surface.blit(highlight, (self.rect.x, self.rect.y))
            text_color = self.colors['text'] if self.state != 'pressed' else (200, 200, 200)
            text_surf = self.fonts['medium'].render(self.text, True, text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            if self.state == 'pressed':
                text_rect.y += 1   
            surface.blit(text_surf, text_rect)
            border_color = (
                min(255, color[0] + 40),
                min(255, color[1] + 40),
                min(255, color[2] + 40)
            )
            pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=3)
    
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1280, 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Audio Visualizer 1.0.1[312031001171701]")
        self.colors = {
            'background': (29, 33, 45),
            'panel': (40, 46, 52),
            'accent': (84, 186, 255),
            'text': (220, 220, 220),
            'button': (60, 68, 80),
            'button_hover': (84, 186, 255),
            'button_pressed': (50, 120, 180)
        }
        self.fonts = self._init_fonts()
        self.particles = [self.Particle(self.WIDTH, self.HEIGHT) for _ in range(150)]
        self.buttons = self._init_buttons()
        self.noise_offset = 0
        self.cell_size = 20
        self.panel_width, self.panel_height = 800, 500
        self.running = True
        self.clock = pygame.time.Clock()

    def _init_fonts(self):
        """初始化字体"""
        fonts = {}
        try:
            fonts['large'] = pygame.font.Font("Minecraft.ttf", 48)
            fonts['medium'] = pygame.font.Font("Minecraft.ttf", 32)
            fonts['small'] = pygame.font.Font("Minecraft.ttf", 18)
        except:
            fonts['large'] = pygame.font.SysFont('courier', 48, bold=True)
            fonts['medium'] = pygame.font.SysFont('courier', 32, bold=True)
            fonts['small'] = pygame.font.SysFont('courier', 18, bold=True)
        return fonts
    
    def _init_buttons(self):
        """初始化按钮"""
        buttons = [
            self.MindustryButton(self.WIDTH//2 - 150, 250, 300, 50, "Real-time mode", self.fonts, self.colors),
            self.MindustryButton(self.WIDTH//2 - 150, 320, 300, 50, "Audio mode", self.fonts, self.colors),
            self.MindustryButton(self.WIDTH//2 - 150, 390, 300, 50, "Output mode", self.fonts, self.colors),
            self.MindustryButton(self.WIDTH//2 - 150, 460, 300, 50, "Exit", self.fonts, self.colors)
        ]
        return buttons

    def _draw_background(self):
        """绘制背景和噪声网格"""
        self.screen.fill(self.colors['background'])
        for y in range(0, self.HEIGHT, self.cell_size):
            for x in range(0, self.WIDTH, self.cell_size):
                n = pnoise2(x * 0.01, y * 0.01 + self.noise_offset, octaves=1)
                alpha = max(0, min(20, int((n + 0.5) * 30)))
                if alpha > 5:
                    s = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                    s.fill((84, 186, 255, alpha))
                    self.screen.blit(s, (x, y))
    
    def _draw_particles(self):
        """绘制所有粒子"""
        for particle in self.particles:
            particle.draw(self.screen)
    
    def _draw_main_panel(self):
        """绘制主面板"""
        panel = pygame.Surface((self.panel_width, self.panel_height), pygame.SRCALPHA)
        panel.fill((*self.colors['panel'], 220))
        pygame.draw.rect(panel, self.colors['accent'], (0, 0, self.panel_width, self.panel_height), 2)
        pygame.draw.rect(panel, (100, 170, 220), (2, 2, self.panel_width-4, self.panel_height-4), 1)
        self.screen.blit(panel, (self.WIDTH//2 - self.panel_width//2, self.HEIGHT//2 - self.panel_height//2))
    
    def _draw_title(self):
        """绘制标题"""
        title = self.fonts['large'].render("Audio Visualizer", True, self.colors['accent'])
        shadow = self.fonts['large'].render("Audio Visualizer", True, (20, 40, 60))
        self.screen.blit(shadow, (self.WIDTH//2 - title.get_width()//2 + 3, 100 + 3))
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 100))
        version = self.fonts['small'].render("v1.0.1[312031001171701]", True, (150, 150, 150))
        self.screen.blit(version, (self.WIDTH//2 - version.get_width()//2, 160))
    
    def _draw_buttons(self):
        """绘制所有按钮"""
        for button in self.buttons:
            button.draw(self.screen)
    
    def _draw_footer(self):
        """绘制页脚信息"""
        copyright = self.fonts['small'].render("© 2025 Wilber-20130410", True, (100, 100, 120))
        self.screen.blit(copyright, (self.WIDTH//2 - copyright.get_width()//2, self.HEIGHT - 40))
    
    def _handle_events(self):
        """处理事件"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
        for button in self.buttons:
            button.update(mouse_pos, mouse_clicked)
            if mouse_clicked and button.state == 'pressed':
                if button.text == "Exit":
                    self.running = False
                elif button.text == "Real-time mode":
                    visualizer = AudioVisualizer_realtime()
                    visualizer.run()
                elif button.text == "Audio mode":
                    audio_visualizer = AudioVisualizer_Audio()
                    audio_visualizer.run()
                elif button.text == "Output mode":
                    output_visualizer = AudioVisualizer_output()
                    output_visualizer.run()
    
    def _update_particles(self):
        """更新所有粒子"""
        for particle in self.particles:
            particle.update()
    
    def _update_noise(self):
        """更新噪声偏移"""
        self.noise_offset += 0.01
    
    def run(self):
        """运行主循环"""
        while self.running:
            self._handle_events()
            self._update_particles()
            self._update_noise()
            self._draw_background()
            self._draw_particles()
            self._draw_main_panel()
            self._draw_title()
            self._draw_buttons()
            self._draw_footer()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

class AudioVisualizer_start_2:
    """像素工厂风格UI"""

    class AnimatedPixelButton:
        """带有动画效果的像素风格按钮"""
        def __init__(self, x, y, width, height, text, color, hover_color):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.color = color
            self.hover_color = hover_color
            self.is_hovered = False
            self.animation_progress = 0
            self.max_animation = 10
        
        def check_hover(self, pos):
            self.is_hovered = self.rect.collidepoint(pos)
            return self.is_hovered
        
        def is_clicked(self, pos, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return self.rect.collidepoint(pos)
            return False
        
        def draw(self, surface):
            if self.is_hovered and self.animation_progress < self.max_animation:
                self.animation_progress += 1
            elif not self.is_hovered and self.animation_progress > 0:
                self.animation_progress -= 1
            offset = self.animation_progress * 0.5
            pulse = abs(self.animation_progress - self.max_animation//2) * 2
            color = self.hover_color if self.is_hovered else self.color
            rect = self.rect.copy()
            rect.inflate_ip(offset, offset)
            pygame.draw.rect(surface, color, rect)
            border_color = (
                min(255, color[0] + 50 + pulse),
                min(255, color[1] + 50 + pulse),
                min(255, color[2] + 50 + pulse)
            )
            pygame.draw.rect(surface, border_color, rect, 2)
            inner_rect = rect.inflate(-4, -4)
            pygame.draw.rect(surface, (0, 0, 0), inner_rect, 1)
            font = pygame.font.SysFont('Arial', 16)
            text_surf = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            surface.blit(text_surf, text_rect)
    
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1280, 720
        self.PIXEL_SIZE = 4
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Audio Visualizer 1.0.1[312031001171701]")
        self.COLORS = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'purple': (128, 0, 128),
            'dark_bg': (10, 10, 20),
            'yellow': (255, 228, 0)
        }
        self.load_resources()
        self.setup_ui()
        
    def load_resources(self):
        """加载字体、音效等资源"""
        try:
            self.font_large = pygame.font.Font("Minecraft.ttf", 48)
            self.font_medium = pygame.font.Font("Minecraft.ttf", 24)
            self.font_small = pygame.font.Font("Minecraft.ttf", 16)
        except:
            self.font_large = pygame.font.SysFont('Arial', 48)
            self.font_medium = pygame.font.SysFont('Arial', 24)
            self.font_small = pygame.font.SysFont('Arial', 16)
            self.button_sound = None

    def setup_ui(self):
        """设置UI元素"""
        self.buttons = [
            self.AnimatedPixelButton(self.WIDTH//2 - 100, 250, 200, 50, "Real-time mode", self.COLORS['green'], (100, 255, 100)),
            self.AnimatedPixelButton(self.WIDTH//2 - 100, 320, 200, 50, "Audio mode", self.COLORS['blue'], (100, 100, 255)),
            self.AnimatedPixelButton(self.WIDTH//2 - 100, 390, 200, 50, "Output mode", self.COLORS['yellow'], (240, 233, 170)),
            self.AnimatedPixelButton(self.WIDTH//2 - 100, 460, 200, 50, "Exit", self.COLORS['red'], (255, 100, 100))
        ]
        self.particles = []
        for _ in range(150):
            self.particles.append({
                'x': random.randint(0, self.WIDTH),
                'y': random.randint(0, self.HEIGHT),
                'speed': random.uniform(0.5, 2.5),
                'size': random.randint(1, 3),
                'color': (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
            })

    def run(self):
        """运行主循环"""
        clock = pygame.time.Clock()
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_clicked = True
            for button in self.buttons:
                button.check_hover(mouse_pos)
                if mouse_clicked and button.is_hovered:
                    if self.button_sound:
                        self.button_sound.play()
                    if button.text == "Exit":
                        running = False
                    elif button.text == "Real-time mode":
                        visualizer = AudioVisualizer_realtime()
                        visualizer.run()
                    elif button.text == "Audio mode":
                        audio_visualizer = AudioVisualizer_Audio()
                        audio_visualizer.run()
                    elif button.text == "Output mode":
                        output_visualizer = AudioVisualizer_output()
                        output_visualizer.run()    
            self.update_particles()
            self.draw_background()
            self.draw_particles()
            self.draw_ui_overlay()
            self.draw_title()
            self.draw_buttons()
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
    
    def update_particles(self):
        """更新粒子位置"""
        for p in self.particles:
            p['y'] += p['speed']
            if p['y'] > self.HEIGHT:
                p['y'] = 0
                p['x'] = random.randint(0, self.WIDTH)
    
    def draw_background(self):
        """绘制像素风格背景"""
        for y in range(self.HEIGHT):
            color_val = max(10, min(50, y // 15))
            pygame.draw.line(
                self.screen, 
                (color_val, color_val, color_val + 10),
                (0, y), (self.WIDTH, y)
            )
    
    def draw_particles(self):
        """绘制粒子"""
        for p in self.particles:
            pygame.draw.circle(
                self.screen, 
                p['color'], 
                (int(p['x']), int(p['y'])), 
                p['size']
            )
    
    def draw_ui_overlay(self):
        """绘制UI覆盖层"""
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 50, 180))
        self.screen.blit(overlay, (0, 0))
    
    def draw_title(self):
        """绘制标题"""
        title = self.font_large.render("Audio Visualizer", True, self.COLORS['white'])
        shadow = self.font_large.render("Audio Visualizer", True, (100, 100, 150))
        self.screen.blit(shadow, (self.WIDTH//2 - title.get_width()//2 + 3, 83))
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 80))
        subtitle = self.font_medium.render("v1.0.1[312031001171701]", True, (200, 200, 255))
        self.screen.blit(subtitle, (self.WIDTH//2 - subtitle.get_width()//2, 140))
        copyright = self.font_small.render("© 2025 Wilber-20130410", True, (100, 100, 120))
        self.screen.blit(copyright, (self.WIDTH//2 - copyright.get_width()//2, self.HEIGHT - 40))
    
    def draw_buttons(self):
        """绘制所有按钮"""
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_hover(mouse_pos)
            button.draw(self.screen)

class AudioVisualizer_realtime:
    """实时音频可视化类"""
    def __init__(self):
        pygame.mixer.music.stop()
        self.WIDTH, self.HEIGHT = 1280, 720
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self._init_pygame()
        self._init_audio_stream()
        self.running = True
    
    def _init_pygame(self):
        """初始化Pygame相关设置"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Audio Visualizer - Real-time Mode")
        self.clock = pygame.time.Clock()
    
    def _init_audio_stream(self):
        """初始化音频流"""
        try:
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
        except Exception as e:
            print(f"初始化音频流错误: {e}")
            self.stream = None
    
    def _process_audio_data(self):
        """处理音频数据并返回FFT结果"""
        if not self.stream:
            return np.zeros(self.CHUNK // 2)
        try:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            data_int = np.frombuffer(data, dtype=np.int16)
            fft = np.abs(np.fft.fft(data_int).real)
            fft = fft[:len(fft) // 2]
            return fft
        except Exception as e:
            print(f"处理音频数据错误: {e}")
            return np.zeros(self.CHUNK // 2)
    
    def _draw_spectrum_bars(self, fft):
        """绘制频谱条"""
        bar_count = min(100, len(fft) // 4)
        bar_width = self.WIDTH / bar_count
        for i in range(bar_count):
            magnitude = min(fft[i * 4] / 1000, self.HEIGHT * 0.8)
            color_value = int(min(magnitude / (self.HEIGHT * 0.8) * 255, 255))
            color = (0, color_value, 255 - color_value)
            pygame.draw.rect(
                self.screen, 
                color,
                (i * bar_width, self.HEIGHT - magnitude, bar_width - 2, magnitude)
            )
    
    def _handle_events(self):
        """处理Pygame事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def run(self):
        """运行主循环"""
        try:
            while self.running:
                self._handle_events()
                fft = self._process_audio_data()
                self.screen.fill((0, 0, 0))
                self._draw_spectrum_bars(fft)
                pygame.display.flip()
                self.clock.tick(60)
        except Exception as e:
            print(f"实时可视化运行错误: {e}")
        finally:
            self._cleanup()
    
    def _cleanup(self):
        """清理资源"""
        try:
            if hasattr(self, 'stream') and self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if hasattr(self, 'p') and self.p:
                self.p.terminate()
        except Exception as e:
            print(f"清理资源错误: {e}")
        pygame.quit()

class AudioVisualizer_output:
    '''输出音频可视化类'''
    def __init__(self):
        pygame.mixer.music.stop()
        self.WIDTH, self.HEIGHT = 1280, 720
        self.CHUNK = 2048
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.BAR_COUNT = 60
        self._init_pygame()
        self._init_audio()
        self.running = True
        self.fps = 60
    
    def _init_pygame(self):
        """初始化Pygame"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Audio Visualizer - Output Mode")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 18)
    
    def _init_audio(self):
        """初始化音频流"""
        try:
            self.p = pyaudio.PyAudio()
            self.output_device_index = None
            info = self.p.get_host_api_info_by_index(0)
            num_devices = info.get('deviceCount')
            for i in range(num_devices):
                device = self.p.get_device_info_by_host_api_device_index(0, i)
                if device['maxOutputChannels'] > 0:
                    self.output_device_index = i
                    break
            if self.output_device_index is None:
                print("未找到输出设备，使用默认设备")
                self.output_device_index = self.p.get_default_output_device_info()['index']
            self.stream = self.p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                input_device_index=self.output_device_index,
                frames_per_buffer=self.CHUNK
            )
        except Exception as e:
            print(f"初始化音频输出错误: {e}")
            self.stream = None
    
    def _get_audio_data(self):
        """获取并处理音频数据"""
        if not self.stream:
            return np.zeros(self.CHUNK)
        try:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            if self.CHANNELS == 2:
                left = audio_data[0::2]
                right = audio_data[1::2]
                audio_data = (left + right) / 2
            return audio_data
        except Exception as e:
            print(f"获取音频数据错误: {e}")
            return np.zeros(self.CHUNK)
    
    def _apply_fft(self, audio_data):
        """应用FFT变换"""
        window = np.hanning(len(audio_data))
        audio_data = audio_data * window
        fft = np.abs(np.fft.rfft(audio_data))
        freqs = np.fft.rfftfreq(len(audio_data), 1.0/self.RATE)
        return fft, freqs
    
    def _group_frequencies(self, fft, freqs):
        """将频率分组为可视化的频带"""
        bands = np.logspace(
            np.log10(20),
            np.log10(20000), 
            num=self.BAR_COUNT
        )
        band_values = []
        for i in range(len(bands)-1):
            mask = (freqs >= bands[i]) & (freqs < bands[i+1])
            if np.any(mask):
                value = np.mean(fft[mask])
                band_values.append(value)
            else:
                band_values.append(0)
        if len(band_values) > 0:
            max_value = np.max(band_values) if np.max(band_values) > 0 else 1
            band_values = [min(value / max_value, 1.0) for value in band_values]
        return band_values
    
    def _draw_visualization(self, band_values):
        """绘制可视化效果"""
        self.screen.fill((0, 0, 20))
        bar_width = self.WIDTH / self.BAR_COUNT
        for i, value in enumerate(band_values):
            height = min(value * self.HEIGHT * 0.8, self.HEIGHT * 0.8)
            color_value = min(255, int(value * 255 * 2))
            color = (color_value, 100, 255 - color_value)
            
            pygame.draw.rect(
                self.screen,
                color,
                (i * bar_width, self.HEIGHT - height, bar_width - 2, height)
            )
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))
        info_text = self.font.render("Output Mode - Press ESC to exit", True, (255, 255, 255))
        self.screen.blit(info_text, (10, 40))
    
    def _handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def run(self):
        """主循环"""
        try:
            while self.running:
                self._handle_events()
                audio_data = self._get_audio_data()
                fft, freqs = self._apply_fft(audio_data)
                band_values = self._group_frequencies(fft, freqs)
                self._draw_visualization(band_values)
                pygame.display.flip()
                self.clock.tick(self.fps)
        except Exception as e:
            print(f"输出可视化运行错误: {e}")
        finally:
            self._cleanup()
    
    def _cleanup(self):
        """清理资源"""
        try:
            if hasattr(self, 'stream') and self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if hasattr(self, 'p') and self.p:
                self.p.terminate()
        except Exception as e:
            print(f"清理资源错误: {e}")
        pygame.quit()

class AudioVisualizer_Audio:
    """音频文件可视化类"""
    def __init__(self, chunk=2048, format=pyaudio.paInt16, channels=2, rate=44100):
        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate
        self.playing = False
        self.paused = False
        self.audio_file = None
        self.p = None
        self.stream = None
        self.current_audio_data = np.zeros(chunk)
        self.lock = threading.Lock()
        try:
            pygame.mixer.init(frequency=rate, size=-16, channels=channels, buffer=chunk)
        except Exception as e:
            print(f"初始化mixer错误: {e}")
        self._init_matplotlib()
    
    def _init_matplotlib(self):
        """初始化matplotlib图形"""
        plt.rcParams['toolbar'] = 'None'
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 8))
        self.fig.canvas.manager.set_window_title('Audio Visualizer - Audio File Mode')
        self.fig.subplots_adjust(hspace=0.5)
        self.x = np.arange(0, self.chunk)
        self.line, = self.ax1.plot(self.x, np.zeros(self.chunk), 'b-', linewidth=0.5)
        self.ax1.set_title('Audio Waveform')
        self.ax1.set_xlabel('Samples')
        self.ax1.set_ylabel('Amplitude')
        self.ax1.set_ylim(-32768, 32767)
        self.ax1.set_xlim(0, self.chunk)
        self.ax1.grid(True, alpha=0.3)
        self.freqs = np.fft.rfftfreq(self.chunk, 1/self.rate)
        self.line_fft, = self.ax2.semilogx(self.freqs, np.zeros(len(self.freqs)), 'r-', linewidth=0.5)
        self.ax2.set_title('Frequency Spectrum')
        self.ax2.set_xlabel('Frequency (Hz)')
        self.ax2.set_ylabel('Amplitude')
        self.ax2.set_xlim(20, self.rate/2)
        self.ax2.set_ylim(0, 1)
        self.ax2.grid(True, alpha=0.3)
        self._add_controls()
        self._init_audio_stream()
        self.set_volume(0.7)
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=50, blit=True, cache_frame_data=False)
    
    def _add_controls(self):
        """添加控制按钮"""
        self.btn_ax = self.fig.add_axes([0.8, 0.02, 0.15, 0.06])
        self.btn = plt.Button(self.btn_ax, 'Play/Pause')
        self.btn.on_clicked(self.toggle_play_pause)
        self.stop_ax = self.fig.add_axes([0.6, 0.02, 0.15, 0.06])
        self.stop_btn = plt.Button(self.stop_ax, 'Stop')
        self.stop_btn.on_clicked(self.stop)
        self.file_ax = self.fig.add_axes([0.4, 0.02, 0.15, 0.06])
        self.file_btn = plt.Button(self.file_ax, 'Select File')
        self.file_btn.on_clicked(self.select_file)
        self.vol_ax = self.fig.add_axes([0.1, 0.02, 0.2, 0.06])
        self.vol_slider = plt.Slider(self.vol_ax, 'Volume', 0.0, 1.0, valinit=0.7)
        self.vol_slider.on_changed(self.set_volume)
    
    def _init_audio_stream(self):
        """初始化音频流"""
        try:
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                output=False,
                frames_per_buffer=self.chunk,
                stream_callback=self.audio_callback
            )
            self.stream.start_stream()
        except Exception as e:
            print(f"创建音频流错误: {e}")
            print("可视化可能无法正常工作。请检查音频设置。")
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """音频回调函数，用于捕获音频数据"""
        if self.playing and not self.paused:
            try:
                audio_data = np.frombuffer(in_data, dtype=np.int16)
                with self.lock:
                    data_length = min(len(audio_data), len(self.current_audio_data))
                    self.current_audio_data[:data_length] = audio_data[:data_length]
            except Exception as e:
                print(f"音频回调错误: {e}")
        return (in_data, pyaudio.paContinue)
    
    def select_file(self, event=None):
        """打开文件选择对话框"""
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file_path = filedialog.askopenfilename(
            title="选择音频文件",
            filetypes=[
                ("音频文件", "*.wav *.mp3 *.ogg *.flac"),
                ("WAV文件", "*.wav"),
                ("MP3文件", "*.mp3"),
                ("OGG文件", "*.ogg"),
                ("FLAC文件", "*.flac"),
                ("所有文件", "*.*")
            ]
        )
        root.destroy()
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        """加载音频文件"""
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return
        if self.playing:
            self.stop()
        self.audio_file = file_path
        try:
            pygame.mixer.music.load(file_path)
            print(f"已加载文件: {os.path.basename(file_path)}")
            self.fig.suptitle(f"Audio File: {os.path.basename(file_path)}", fontsize=12)
        except Exception as e:
            print(f"加载文件失败: {e}")
    
    def toggle_play_pause(self, event = None):
        """切换播放/暂停状态"""
        if not self.audio_file:
            print("请先选择音频文件")
            return
        if not self.playing:
            self.play()
        else:
            if self.paused:
                self.unpause()
            else:
                self.pause()
    
    def play(self):
        """开始播放音频"""
        if not self.audio_file:
            print("请先选择音频文件")
            return
        try:
            pygame.mixer.music.play()
            self.playing = True
            self.paused = False
            self.btn.label.set_text('Pause')
            print("开始播放")
        except Exception as e:
            print(f"开始播放错误: {e}")
    
    def pause(self):
        """暂停播放"""
        try:
            pygame.mixer.music.pause()
            self.paused = True
            self.btn.label.set_text('Resume')
            print("播放暂停")
        except Exception as e:
            print(f"暂停播放错误: {e}")
    
    def unpause(self):
        """继续播放"""
        try:
            pygame.mixer.music.unpause()
            self.paused = False
            self.btn.label.set_text('Pause')
            print("继续播放")
        except Exception as e:
            print(f"继续播放错误: {e}")
    
    def stop(self, event=None):
        """停止播放"""
        try:
            pygame.mixer.music.stop()
            self.playing = False
            self.paused = False
            self.btn.label.set_text('Play/Pause')
            with self.lock:
                self.current_audio_data = np.zeros(self.chunk)
            print("播放停止")
        except Exception as e:
            print(f"停止播放错误: {e}")
    
    def set_volume(self, val):
        """设置音量"""
        try:
            pygame.mixer.music.set_volume(val)
        except Exception as e:
            print(f"设置音量错误: {e}")
    
    def update_plot(self, frame):
        """更新可视化图表"""
        with self.lock:
            audio_data = self.current_audio_data.copy()
        self.line.set_ydata(audio_data)
        if np.max(np.abs(audio_data)) > 0:
            try:
                window = np.hanning(len(audio_data))
                windowed_data = audio_data * window
                fft_data = np.abs(np.fft.rfft(windowed_data))
                if np.max(fft_data) > 0:
                    fft_normalized = fft_data / np.max(fft_data)
                    self.line_fft.set_ydata(fft_normalized)
            except Exception as e:
                pass
        return self.line, self.line_fft

    def run(self):
        """运行应用程序"""
        try:
            plt.show(block=True)
        except Exception as e:
            print(f"运行应用程序错误: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """清理资源"""
        try:
            self.stop()
            if hasattr(self, 'stream') and self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if hasattr(self, 'p') and self.p:
                self.p.terminate()
            pygame.mixer.quit()
            plt.close('all')
        except Exception as e:
            print(f"清理资源错误: {e}")

def load_music():
    """加载音乐"""
    try:
        pygame.init()
        mixer.init()
        if os.path.exists("minecraft_title.ogg"):
            mixer.music.load("minecraft_title.ogg")
            mixer.music.play(-1)
        else:
            print("背景音乐文件 minecraft_title.ogg 不存在")
    except Exception as e:
        print(f"加载音乐错误: {e}")

def check_network():
    """检查网络连接"""
    global wifi
    try:
        requests.get('https://www.baidu.com', timeout=3)
        wifi = True
        return True
    except:
        wifi = False
        return False

if __name__ == "__main__":
    check_network()
    load_music()
    t = time.localtime()
    print(f'time:{t.tm_year}.{t.tm_mon}.{t.tm_mday}.{t.tm_hour}:{t.tm_min}:{t.tm_sec}')
    app = AudioVisualizerLauncher()
    app.run()
