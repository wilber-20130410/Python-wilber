# -*- coding: utf-8 -*-
'''
名称:音频可视化
作者:wilber-20130410
版本:1.0.0[312030826143301](正式版)
日期:2025.8.26
留言:
1.使用者需要具有python3基础,并有以下所使用的各种库的基础。
2.使用前请阅读这段注释,和第802、834、840行的注释。
3.Linux(Ubuntu)系统需要确保jack服务的运行。
4.使用前请确保已经安装以下所使用的库。
5.本人推荐使用Visual Studio Code或PyCharm Community作为IDE(集成开发环境)。
6.需要安装python3及以上python环境(本人使用python3.12.3)。
7.本代码无法直接使用，请根据自身情况进行调整。
8.AudioVisualizer_output()模块的功能若无法使用为正常现象，本人也无力解决。
9.字体和背景音乐要放在工作目录中,即IDE所打开的目录,或命令行所在的目录。
10.以上留言不分先后。
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

class AudioVisualizerLauncher:
    def __init__(self):
        # 初始化pygame
        pygame.init()
        mixer.init()
        # 屏幕设置
        self.WIDTH, self.HEIGHT = 854, 480
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("AudioVisualizer 1.0.0[312030826143301]")
        # 颜色定义
        self.BLACK = (0, 0, 0)
        self.DARK_GREEN = (0, 71, 0)
        self.GREEN = (0, 100, 0)
        self.LIGHT_GREEN = (100, 200, 100)
        self.WHITE = (255, 255, 255)
        self.GRAY = (100, 100, 100)
        self.LIGHT_GRAY = (200, 200, 200)
        # 加载字体
        self._load_fonts()
        # 初始化背景
        self.background_layers = []
        self.layer_positions = [0, 0, 0]
        self._init_background()
        # 初始化标题
        self.title_text = self.title_font.render("AudioVisualizer", True, self.WHITE)
        self.title_shadow = self.title_font.render("AudioVisualizer", True, self.GRAY)
        self.title_rect = self.title_text.get_rect(center=(self.WIDTH//2, self.HEIGHT//3))
        # 初始化版本信息
        self.version_text = self.version_font.render("1.0.0[312030826143301]", True, self.LIGHT_GRAY)
        self.version_rect = self.version_text.get_rect(bottomright=(self.WIDTH-10, self.HEIGHT-10))
        # 初始化进度条
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
        # 游戏状态
        self.running = True
        self.clock = pygame.time.Clock()
        self.start_time = time.time()

    def game_stop(self):
        mixer.music.stop()
        AudioVisualizerLauncher.current_loading_text = "Network anomaly , please check the network and restart"
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
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
        if self.progress < 5:
            self.current_loading_text = self.loading_texts[0]
        elif 5 <= self.progress < 15:
            if wifi == True:
                self.current_loading_text = self.loading_texts[1]
            elif wifi == False:
                self.current_loading_text = "Network anomaly , please check the network and restart"
        elif 15 <= self.progress < 25:
            if wifi == True:
                self.current_loading_text = self.loading_texts[2]
            elif wifi == False:
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
        # 进度条背景
        pygame.draw.rect(self.screen, self.GRAY, self.progress_rect)
        # 进度条填充
        filled_rect = pygame.Rect(
            self.progress_rect.x, 
            self.progress_rect.y, 
            self.progress_rect.width * (self.progress / 100), 
            self.progress_rect.height
        )
        pygame.draw.rect(self.screen, self.GREEN, filled_rect)
        pygame.draw.rect(self.screen, self.LIGHT_GREEN, filled_rect, 1)
        # 加载文本
        loading_surface = self.progress_font.render(self.current_loading_text, True, self.LIGHT_GRAY)
        loading_rect = loading_surface.get_rect(midbottom=(self.WIDTH//2, self.progress_rect.y - 10))
        self.screen.blit(loading_surface, loading_rect)
        # 完成提示
        if self.progress >= 100:
            continue_text = self.progress_font.render("Louding", True, self.LIGHT_GREEN)
            continue_rect = continue_text.get_rect(midtop=(self.WIDTH//2, self.progress_rect.bottom + 20))
            self.screen.blit(continue_text, continue_rect)
            self.running = False
    
    def _draw_version(self):
        """绘制版本信息"""
        self.screen.blit(self.version_text, self.version_rect)
    
    def _update(self):
        """更新游戏状态"""
        self._update_background()
        self._update_progress()
    
    def _draw(self):
        """绘制游戏"""
        self.screen.fill(self.DARK_GREEN)
        self._draw_background()
        self._draw_title()
        self._draw_progress_bar()
        self._draw_version()
        pygame.display.flip()
    
    def run_game(self):
        start = [1, 2 ,3 ,4 ,5, 6]
        random.shuffle(start)
        stnum = random.choice(start)
        if stnum % 2 == 1:
            if __name__ == "__main__":
                app = PixelFactoryUI()
                app.run()
        else:
            if __name__ == "__main__":
                app_1 = AudioVisualizer()
                app_1.run()

    def run(self):
        """运行游戏主循环"""
        while self.running == True:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
        self.run_game()
        pygame.quit()

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
        # 边界检查
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
        # 动画更新
        if self.state == 'hover' and self.animation < 10:
            self.animation += 1
        elif self.state == 'pressed' and self.animation > -5:
            self.animation -= 1
        elif self.state == 'normal' and self.animation > 0:
            self.animation -= 1
            
    def draw(self, surface):
        """绘制按钮"""
        # 确定颜色
        if self.state == 'pressed':
            color = self.colors['button_pressed']
        elif self.state == 'hover':
            color = self.colors['button_hover']
        else:
            color = self.colors['button']
        # 绘制按钮背景
        pygame.draw.rect(surface, color, self.rect, border_radius=3)
        # 绘制高光效果
        highlight = pygame.Surface((self.rect.width, max(2, self.rect.height // 4)), pygame.SRCALPHA)
        highlight.fill((255, 255, 255, 30))
        surface.blit(highlight, (self.rect.x, self.rect.y))
        # 绘制文本
        text_color = self.colors['text'] if self.state != 'pressed' else (200, 200, 200)
        text_surf = self.fonts['medium'].render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        # 添加按下效果偏移
        if self.state == 'pressed':
            text_rect.y += 1   
        surface.blit(text_surf, text_rect)
        # 绘制边框
        border_color = (
            min(255, color[0] + 40),
            min(255, color[1] + 40),
            min(255, color[2] + 40)
        )
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=3)

class AudioVisualizer:
    """音频可视化主类"""
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1280, 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Audio Visualizer 1.0.0[312030826143301]")
        # 颜色定义
        self.colors = {
            'background': (29, 33, 45),
            'panel': (40, 46, 52),
            'accent': (84, 186, 255),
            'text': (220, 220, 220),
            'button': (60, 68, 80),
            'button_hover': (84, 186, 255),
            'button_pressed': (50, 120, 180)
        }
        # 初始化字体
        self.fonts = self._init_fonts()
        # 初始化粒子系统
        self.particles = [Particle(self.WIDTH, self.HEIGHT) for _ in range(150)]
        # 初始化按钮
        self.buttons = self._init_buttons()
        # 背景噪声参数
        self.noise_offset = 0
        self.cell_size = 20
        # 主面板参数
        self.panel_width, self.panel_height = 800, 500
        # 游戏状态
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
            MindustryButton(self.WIDTH//2 - 150, 250, 300, 50, "Real-time mode", self.fonts, self.colors),
            MindustryButton(self.WIDTH//2 - 150, 320, 300, 50, "Audio mode", self.fonts, self.colors),
            MindustryButton(self.WIDTH//2 - 150, 390, 300, 50, "Output mode", self.fonts, self.colors),
            MindustryButton(self.WIDTH//2 - 150, 460, 300, 50, "Exit", self.fonts, self.colors)
        ]
        return buttons

    def _draw_background(self):
        """绘制背景和噪声网格"""
        self.screen.fill(self.colors['background'])
        # 绘制噪声网格
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
        # 面板边框效果
        pygame.draw.rect(panel, self.colors['accent'], (0, 0, self.panel_width, self.panel_height), 2)
        pygame.draw.rect(panel, (100, 170, 220), (2, 2, self.panel_width-4, self.panel_height-4), 1)
        self.screen.blit(panel, (self.WIDTH//2 - self.panel_width//2, self.HEIGHT//2 - self.panel_height//2))
    
    def _draw_title(self):
        """绘制标题"""
        title = self.fonts['large'].render("Audio Visualizer", True, self.colors['accent'])
        shadow = self.fonts['large'].render("Audio Visualizer", True, (20, 40, 60))
        self.screen.blit(shadow, (self.WIDTH//2 - title.get_width()//2 + 3, 100 + 3))
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 100))
        # 版本号
        version = self.fonts['small'].render("v1.0.0[312030826143301]", True, (150, 150, 150))
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
                if event.type == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
        # 更新按钮状态
        for button in self.buttons:
            button.update(mouse_pos, mouse_clicked)
            # 检查按钮点击
            if mouse_clicked and button.state == 'pressed':
                if button.text == "Exit":
                    self.running = False
                elif button.text == "Real-time mode":
                    visualizer = AudioVisualizer_realtime()
                    visualizer.run()
                elif button.text == "Audio mode":
                    AudioVisualizer_Audio().run()
                elif button.text == "Output mode":
                    AudioVisualizer_output().run()
    
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
            # 绘制所有元素
            self._draw_background()
            self._draw_particles()
            self._draw_main_panel()
            self._draw_title()
            self._draw_buttons()
            self._draw_footer()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

class PixelFactoryUI:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1280, 720
        self.PIXEL_SIZE = 4
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Audio Visualizer 1.0.0[312030826143301]")
        # 颜色定义
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
        # 初始化资源
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
        # 加载音效
        if os.path.exists("assets/sounds"):
            self.button_sound = pygame.mixer.Sound("assets/sounds/button.wav")
        else:
            self.button_sound = None

    def setup_ui(self):
        """设置UI元素"""
        # 创建按钮
        self.buttons = [
            AnimatedPixelButton(self.WIDTH//2 - 100, 250, 200, 50, "Real-time mode", self.COLORS['green'], (100, 255, 100)),
            AnimatedPixelButton(self.WIDTH//2 - 100, 320, 200, 50, "Audio mode", self.COLORS['blue'], (100, 100, 255)),
            AnimatedPixelButton(self.WIDTH//2 - 100, 390, 200, 50, "Output mode", self.COLORS['yellow'], (240, 233, 170)),
            AnimatedPixelButton(self.WIDTH//2 - 100, 460, 200, 50, "Exit", self.COLORS['red'], (255, 100, 100))
        ]
        # 初始化粒子系统
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_ESCAPE:
                        running = False
                # 处理按钮点击
                for button in self.buttons:
                    if button.is_clicked(mouse_pos, event):
                        if self.button_sound:
                            self.button_sound.play()
                        if button.text == "Exit":
                            running = False
                        elif button.text == "Real-time mode":
                            visualizer = AudioVisualizer_realtime()
                            visualizer.run()
                        elif button.text == "Audio mode":
                            AudioVisualizer_Audio().run()
                        elif button.text == "Output mode":
                            AudioVisualizer_output().run()
            # 更新粒子
            self.update_particles()
            # 绘制
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
        # 简单的渐变背景
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
        overlay.fill((0, 0, 50, 180))  # 半透明深蓝色
        self.screen.blit(overlay, (0, 0))
    
    def draw_title(self):
        """绘制标题"""
        title = self.font_large.render("Audio Visualizer", True, self.COLORS['white'])
        shadow = self.font_large.render("Audio Visualizer", True, (100, 100, 150))
        # 绘制阴影效果
        self.screen.blit(shadow, (self.WIDTH//2 - title.get_width()//2 + 3, 83))
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 80))
        # 副标题
        subtitle = self.font_medium.render("v1.0.0[312030826143301]", True, (200, 200, 255))
        self.screen.blit(subtitle, (self.WIDTH//2 - subtitle.get_width()//2, 140))
        # 版权信息
        copyright = self.font_small.render("© 2025 Wilber-20130410", True, (100, 100, 120))
        self.screen.blit(copyright, (self.WIDTH//2 - copyright.get_width()//2, self.HEIGHT - 40))
    
    def draw_buttons(self):
        """绘制所有按钮"""
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_hover(mouse_pos)
            button.draw(self.screen)

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
        # 动画效果
        if self.is_hovered and self.animation_progress < self.max_animation:
            self.animation_progress += 1
        elif not self.is_hovered and self.animation_progress > 0:
            self.animation_progress -= 1
        # 计算动画参数
        offset = self.animation_progress * 0.5
        pulse = abs(self.animation_progress - self.max_animation//2) * 2
        # 绘制按钮主体
        color = self.hover_color if self.is_hovered else self.color
        rect = self.rect.copy()
        rect.inflate_ip(offset, offset)
        pygame.draw.rect(surface, color, rect)
        # 绘制像素风格的边框
        border_color = (
            min(255, color[0] + 50 + pulse),
            min(255, color[1] + 50 + pulse),
            min(255, color[2] + 50 + pulse)
        )
        pygame.draw.rect(surface, border_color, rect, 2)
        # 绘制内部边框
        inner_rect = rect.inflate(-4, -4)
        pygame.draw.rect(surface, (0, 0, 0), inner_rect, 1)
        # 绘制文本
        font = pygame.font.SysFont('Arial', 16)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

class AudioVisualizer_realtime:
    """音频可视化主类"""
    def __init__(self):
        # 初始化参数
        pygame.mixer.music.stop ()
        self.WIDTH, self.HEIGHT = 800, 600
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        # 初始化Pygame
        self._init_pygame()
        # 初始化音频流
        self._init_audio_stream()
        # 运行状态
        self.running = True
    
    def _init_pygame(self):
        """初始化Pygame相关设置"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Audio Visualizer 1.0.0[312030826143301]")
    def _init_audio_stream(self):
        """初始化音频流"""
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
    
    def _process_audio_data(self):
        """处理音频数据并返回FFT结果"""
        # 读取音频数据
        data = self.stream.read(self.CHUNK, exception_on_overflow=False)
        data_int = np.frombuffer(data, dtype=np.int16)
        # 计算FFT
        fft = np.abs(np.fft.fft(data_int).real)
        fft = fft[:len(fft) // 2]  # 取前半部分（对称）
        return fft
    
    def _draw_spectrum_bars(self, fft):
        """绘制频谱条"""
        bar_width = self.WIDTH / (len(fft) // 16)  # 减少条数
        for i in range(len(fft) // 16):
            magnitude = fft[i * 16] / 500  # 缩放因子
            pygame.draw.rect(
                self.screen, 
                (0, 255, 0),
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
                fft = self._process_audio_data()# 处理音频数据
                self.screen.fill((0, 0, 0))# 清屏
                self._draw_spectrum_bars(fft)# 绘制频谱
                pygame.display.flip()# 更新显示
        finally:
            self._cleanup()
    
    def _cleanup(self):
        """清理资源"""
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        pygame.quit()

class AudioVisualizer_output:
    '''wilber-20130410:本功能若无法使用为正常现象，本人也无力解决'''
    def __init__(self):
        # 初始化参数
        pygame.mixer.music.stop ()
        self.WIDTH, self.HEIGHT = 1200, 600
        self.CHUNK = 2048  # 更大的块减少延迟
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2   # 立体声
        self.RATE = 44100
        self.BAR_COUNT = 60 # 显示的频带数量
        # 初始化
        self._init_pygame()
        self._init_audio()
        # 运行状态
        self.running = True
        self.fps = 60
    
    def _init_pygame(self):
        """初始化Pygame"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Audio Visualizer 1.0.0[312030826143301]")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 18)
    
    def _init_audio(self):
        """初始化音频流"""
        self.p = pyaudio.PyAudio()
        # 获取输出设备信息
        info = self.p.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        self.output_device_index = None
        for i in range(num_devices):         #wilber-20130410：进行识别，获取可用音频设备，也可以手动设置
            device = self.p.get_device_info_by_host_api_device_index(0, i)
            if device['maxOutputChannels'] > 0:
                self.output_device_index = device
                break
#        self.output_device_index = 0
        # wilber-20130410：所需设备为声卡（同时支持输入和输出），Windows系统需开启立体声混响，Linux（Ubuntu）需确保jack服务正常运行
        if self.output_device_index is None:
            print("未找到输出设备!")
        # 打开输入流捕获扬声器输出
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            input_device_index=self.output_device_index,
            frames_per_buffer=self.CHUNK
        )
    
    def _get_audio_data(self):
        """获取并处理音频数据"""
        try:
            # 读取音频数据
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            # 分离左右声道
            if self.CHANNELS == 2:
                left = audio_data[0::2]
                right = audio_data[1::2]
                # 合并为单声道
                audio_data = (left + right) / 2
            return audio_data
        except Exception as e:
            print(f"音频捕获错误: {e}")
            return np.zeros(self.CHUNK)
    
    def _apply_fft(self, audio_data):
        """应用FFT变换"""
        # 加汉宁窗减少频谱泄漏
        window = np.hanning(len(audio_data))
        audio_data = audio_data * window
        # 计算FFT
        fft = np.abs(np.fft.rfft(audio_data))
        freqs = np.fft.rfftfreq(len(audio_data), 1.0/self.RATE)
        return fft, freqs
    
    def _group_frequencies(self, fft, freqs):
        """将频率分组为可视化的频带"""
        # 创建对数分布的频带
        bands = np.logspace(
            np.log10(20),  # 20Hz起始
            np.log10(20000),  # 20kHz结束
            num=self.BAR_COUNT
        )
        band_values = []
        for i in range(len(bands)-1):
            # 找到当前频带范围内的FFT值
            mask = (freqs >= bands[i]) & (freqs < bands[i+1])
            if np.any(mask):
                # 取该频带的平均值
                value = np.mean(fft[mask])
                band_values.append(value)
            else:
                band_values.append(0)
        # 归一化
        max_value = np.max(band_values) if np.max(band_values) > 0 else 1
        band_values = band_values / max_value
        return band_values
    
    def _draw_visualization(self, band_values):
        """绘制可视化效果"""
        # 清屏
        self.screen.fill((0, 0, 20))
        # 绘制频谱条
        bar_width = self.WIDTH / self.BAR_COUNT
        for i, value in enumerate(band_values):
            # 计算高度 (限制最大高度为屏幕的80%)
            height = min(value * self.HEIGHT * 0.8, self.HEIGHT * 0.8)
            # 计算颜色 (从蓝到红渐变)
            color_value = min(255, int(value * 255 * 2))
            color = (color_value, 100, 255 - color_value)
            # 绘制频带
            pygame.draw.rect(
                self.screen,
                color,
                (i * bar_width, self.HEIGHT - height, bar_width - 2, height)
            )
        # 绘制信息
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))
    
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
                audio_data = self._get_audio_data()# 获取音频数据
                fft, freqs = self._apply_fft(audio_data)# 应用FFT
                band_values = self._group_frequencies(fft, freqs)# 分组频率
                self._draw_visualization(band_values)# 绘制可视化
                # 更新显示
                pygame.display.flip()
                self.clock.tick(self.fps)
        finally:
            self._cleanup()
    
    def _cleanup(self):
        """清理资源"""
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        pygame.quit()
        sys.exit()

class AudioVisualizer_Audio:
    def __init__(self, chunk=2048, format=pyaudio.paInt16, channels=2, rate=44100):
        """
        初始化音频播放和可视化器
        
        参数:
            chunk: 音频数据块大小
            format: 音频格式
            channels: 声道数
            rate: 采样率
        """
        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate
        self.playing = False
        self.paused = False
        self.audio_file = None
        # PyAudio实例
        self.p = pyaudio.PyAudio()
        # 初始化pygame mixer
        pygame.mixer.init(frequency=rate, size=-16, channels=channels, buffer=chunk)
        # 音频数据共享变量
        self.current_audio_data = np.zeros(chunk)
        self.lock = threading.Lock()
        # 设置matplotlib
        plt.rcParams['toolbar'] = 'None'
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 8))
        self.fig.canvas.manager.set_window_title('Audio Visualizer 1.0.0[312030826143301]')
        self.fig.subplots_adjust(hspace=0.5)
        # 初始化波形图
        self.x = np.arange(0, chunk)
        self.line, = self.ax1.plot(self.x, np.zeros(chunk), 'b-')
        self.ax1.set_title('Audio Waveform')
        self.ax1.set_xlabel('Samples')
        self.ax1.set_ylabel('Amplitude')
        self.ax1.set_ylim(-32768, 32767)
        self.ax1.set_xlim(0, chunk)
        # 初始化频谱图
        self.freqs = np.fft.rfftfreq(chunk, 1/rate)
        self.line_fft, = self.ax2.semilogx(self.freqs, np.zeros(len(self.freqs)), 'r-')
        self.ax2.set_title('Frequency Spectrum')
        self.ax2.set_xlabel('Frequency (Hz)')
        self.ax2.set_ylabel('Amplitude (dB)')
        self.ax2.set_xlim(20, rate/2)
        self.ax2.set_ylim(0, 1)
        # 添加控制按钮
        self.btn_ax = self.fig.add_axes([0.8, 0.02, 0.15, 0.06])
        self.btn = plt.Button(self.btn_ax, 'Play/Pause')
        self.btn.on_clicked(self.toggle_play_pause)
        # 添加停止按钮
        self.stop_ax = self.fig.add_axes([0.6, 0.02, 0.15, 0.06])
        self.stop_btn = plt.Button(self.stop_ax, 'Stop')
        self.stop_btn.on_clicked(self.stop)
        # 添加文件选择按钮
        self.file_ax = self.fig.add_axes([0.4, 0.02, 0.15, 0.06])
        self.file_btn = plt.Button(self.file_ax, 'Select File')
        self.file_btn.on_clicked(self.select_file)
        # 添加音量控制
        self.vol_ax = self.fig.add_axes([0.1, 0.02, 0.2, 0.06])
        self.vol_slider = plt.Slider(self.vol_ax, 'Volume', 0.0, 1.0, valinit=0.7)
        self.vol_slider.on_changed(self.set_volume)
        # 创建音频流用于捕获播放的音频
        try:
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
            self.stream = None
        # 设置初始音量
        self.set_volume(0.7)
        # 动画
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=50, blit=True)
        mixer.music.stop()
        
    def audio_callback(self, in_data, frame_count, time_info, status):
        """音频回调函数，用于捕获音频数据"""
        if self.playing and not self.paused:
            # 将字节数据转换为numpy数组
            try:
                audio_data = np.frombuffer(in_data, dtype=np.int16)
                # 更新当前音频数据
                with self.lock:
                    # 确保不超出数组边界
                    data_length = min(len(audio_data), len(self.current_audio_data))
                    self.current_audio_data[:data_length] = audio_data[:data_length]
            except Exception as e:
                print(f"音频回调错误: {e}")
        return (in_data, pyaudio.paContinue)
    
    def select_file(self, event=None):
        """打开文件选择对话框"""
        root = Tk()
        root.withdraw()  # 隐藏主窗口
        file_path = filedialog.askopenfilename(
            title="选择音频文件",
            filetypes=[("音频文件", "*.wav *.mp3 *.ogg *.flac")]
        )
        root.destroy()
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        """加载音频文件"""
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return
        # 停止当前播放（如果有）
        if self.playing:
            self.stop()
        self.audio_file = file_path
        try:
            pygame.mixer.music.load(file_path)
            print(f"已加载文件: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"加载文件失败: {e}")
    
    def toggle_play_pause(self, event=None):
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
            # 重置音频数据
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
        # 获取当前音频数据
        with self.lock:
            audio_data = self.current_audio_data.copy()
        # 更新波形图
        self.line.set_ydata(audio_data)
        # 计算并更新频谱图
        if np.max(np.abs(audio_data)) > 0:  # 确保有音频数据
            try:
                # 应用汉宁窗减少频谱泄漏
                window = np.hanning(len(audio_data))
                windowed_data = audio_data * window
                # 计算FFT
                fft_data = np.abs(np.fft.rfft(windowed_data))
                # 转换为分贝
                fft_db = 20 * np.log10(fft_data + 1e-6)  # 加上小值避免log(0)
                fft_db_normalized = (fft_db - np.min(fft_db)) / (np.max(fft_db) - np.min(fft_db) + 1e-6)
                self.line_fft.set_ydata(fft_db_normalized)
            except Exception as e:
                # 可视化错误的静默处理
                pass
        return self.line, self.line_fft

    def run(self):
        """运行应用程序"""
        try:
            plt.show()
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
        except Exception as e:
            print(f"清理资源错误: {e}")
    
    def __del__(self):
        """析构函数用于清理"""
        self.cleanup()

def load_music():
    """加载音乐"""
    pygame.init()
    mixer.music.load("minecraft_title.ogg")
    mixer.music.play(-1)

try:
    requests.get('https://www.baidu.com', timeout=3)
    wifi = True
except:
    wifi = False
load_music()
t = time.localtime()
year = t[0]
month = t[1]
day= t[2]
hour = t[3]
minute = t[4]
sec = t[5]
print('time:%d.%d.%d.%d:%d:%d' % (year, month, day, hour, minute, sec))
if __name__ == "__main__":
    app = AudioVisualizerLauncher()
    app.run()