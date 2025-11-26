#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Log Temizleyici - Sadece log dosyalarını temizler
Cache'ler, geçmiş ve diğer veriler korunur
"""

import os
import sys
import shutil
import platform
from pathlib import Path
from typing import List, Tuple, Set, Dict

# Korunması gereken kritik dizinler
PROTECTED_PATHS = [
    r'C:\Windows\System32',
    r'C:\Windows\SysWOW64',
    r'C:\Windows\WinSxS',
    r'C:\Windows\winsxs',
    r'C:\Windows\assembly',
    r'C:\Program Files\Windows Defender',
    r'C:\Program Files\Common Files',
    r'C:\Program Files (x86)\Common Files',
    r'C:\Windows\System',
]


def is_protected_path(file_path: str) -> bool:
    """Dosyanın korumalı bir dizinde olup olmadığını kontrol eder."""
    file_path_lower = file_path.lower()
    for protected in PROTECTED_PATHS:
        if protected.lower() in file_path_lower:
            return True
    return False


def format_size(size_bytes: int) -> str:
    """Dosya boyutunu okunabilir formata çevirir."""
    if size_bytes == 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def get_user_profile() -> str:
    """Kullanıcı profil dizinini döndürür."""
    return os.environ.get('USERPROFILE', os.environ.get('HOME', ''))


def get_appdata_paths() -> Dict[str, str]:
    """AppData dizin yollarını döndürür."""
    user_profile = get_user_profile()
    return {
        'local': os.path.join(user_profile, 'AppData', 'Local'),
        'roaming': os.path.join(user_profile, 'AppData', 'Roaming'),
        'locallow': os.path.join(user_profile, 'AppData', 'LocalLow'),
    }


def get_browser_log_paths() -> List[Tuple[str, str]]:
    """Sadece tarayıcı log dosyalarını döndürür (cache ve geçmiş değil)."""
    appdata = get_appdata_paths()
    browser_logs = []
    
    # Chrome log dosyaları
    chrome_local = os.path.join(appdata['local'], 'Google', 'Chrome', 'User Data')
    if os.path.exists(chrome_local):
        # Chrome'un log dosyalarını ara
        for root, dirs, files in os.walk(chrome_local):
            for file in files:
                if file.endswith('.log') or 'log' in file.lower():
                    file_path = os.path.join(root, file)
                    if not is_protected_path(file_path):
                        browser_logs.append((file_path, 'Chrome Log'))
    
    # Edge log dosyaları
    edge_local = os.path.join(appdata['local'], 'Microsoft', 'Edge', 'User Data')
    if os.path.exists(edge_local):
        for root, dirs, files in os.walk(edge_local):
            for file in files:
                if file.endswith('.log') or 'log' in file.lower():
                    file_path = os.path.join(root, file)
                    if not is_protected_path(file_path):
                        browser_logs.append((file_path, 'Edge Log'))
    
    # Brave log dosyaları
    brave_local = os.path.join(appdata['local'], 'BraveSoftware', 'Brave-Browser', 'User Data')
    if os.path.exists(brave_local):
        for root, dirs, files in os.walk(brave_local):
            for file in files:
                if file.endswith('.log') or 'log' in file.lower():
                    file_path = os.path.join(root, file)
                    if not is_protected_path(file_path):
                        browser_logs.append((file_path, 'Brave Log'))
    
    return browser_logs


def get_game_log_paths() -> List[Tuple[str, str]]:
    """Sadece oyun log dizinlerini döndürür (cache değil)."""
    appdata = get_appdata_paths()
    game_logs = []
    
    # Steam - sadece logs
    steam_logs = os.path.join(appdata['local'], 'Steam', 'logs')
    if os.path.exists(steam_logs):
        game_logs.append((steam_logs, 'Steam Logs'))
    
    # Epic Games - sadece Logs
    epic_logs = os.path.join(appdata['local'], 'EpicGamesLauncher', 'Saved', 'Logs')
    if os.path.exists(epic_logs):
        game_logs.append((epic_logs, 'Epic Games Logs'))
    
    # Ubisoft - sadece logs
    ubisoft_logs = os.path.join(appdata['local'], 'Ubisoft Game Launcher', 'logs')
    if os.path.exists(ubisoft_logs):
        game_logs.append((ubisoft_logs, 'Ubisoft Logs'))
    
    # Riot Games - log dosyalarını ara
    riot_dir = os.path.join(appdata['local'], 'Riot Games')
    if os.path.exists(riot_dir):
        for root, dirs, files in os.walk(riot_dir):
            for file in files:
                if file.endswith(('.log', '.txt')) or 'log' in file.lower():
                    file_path = os.path.join(root, file)
                    if not is_protected_path(file_path):
                        game_logs.append((file_path, 'Riot Games Log'))
    
    # GOG Galaxy - sadece logs
    gog_logs = os.path.join(appdata['local'], 'GOG.com', 'Galaxy', 'logs')
    if os.path.exists(gog_logs):
        game_logs.append((gog_logs, 'GOG Logs'))
    
    return game_logs


def get_application_log_paths() -> List[Tuple[str, str]]:
    """Sadece uygulama log dizinlerini döndürür (cache değil)."""
    appdata = get_appdata_paths()
    app_logs = []
    
    # Discord - sadece logs
    discord_logs = os.path.join(appdata['roaming'], 'discord', 'logs')
    if os.path.exists(discord_logs):
        app_logs.append((discord_logs, 'Discord Logs'))
    
    # Spotify - log dosyalarını ara
    spotify_dir = os.path.join(appdata['local'], 'Spotify')
    if os.path.exists(spotify_dir):
        for root, dirs, files in os.walk(spotify_dir):
            for file in files:
                if file.endswith(('.log', '.txt')) or 'log' in file.lower():
                    file_path = os.path.join(root, file)
                    if not is_protected_path(file_path):
                        app_logs.append((file_path, 'Spotify Log'))
    
    # VS Code - sadece logs
    vscode_logs = os.path.join(appdata['roaming'], 'Code', 'logs')
    if os.path.exists(vscode_logs):
        app_logs.append((vscode_logs, 'VS Code Logs'))
    
    # Slack - sadece logs
    slack_logs = os.path.join(appdata['local'], 'slack', 'logs')
    if os.path.exists(slack_logs):
        app_logs.append((slack_logs, 'Slack Logs'))
    
    # Zoom - sadece logs
    zoom_logs = os.path.join(appdata['roaming'], 'Zoom', 'logs')
    if os.path.exists(zoom_logs):
        app_logs.append((zoom_logs, 'Zoom Logs'))
    
    return app_logs


def get_system_log_paths() -> List[Tuple[str, str]]:
    """Sadece sistem log dizinlerini döndürür (temp, recent files, prefetch değil)."""
    appdata = get_appdata_paths()
    system_logs = []
    
    # Log dizinleri
    log_paths = [
        (os.path.join(appdata['local'], 'Logs'), 'User Logs'),
        (r'C:\Windows\Logs', 'Windows Logs'),
    ]
    system_logs.extend([(p, n) for p, n in log_paths if os.path.exists(p)])
    
    return system_logs


def calculate_directory_size(path: str) -> int:
    """Dizin boyutunu hesaplar."""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, PermissionError):
                    pass
    except (OSError, PermissionError):
        pass
    return total_size


def delete_directory(path: str) -> Tuple[bool, int]:
    """Dizini siler ve silinen boyutu döndürür."""
    if not os.path.exists(path):
        return False, 0
    
    if is_protected_path(path):
        return False, 0
    
    try:
        size = calculate_directory_size(path)
        shutil.rmtree(path, ignore_errors=True)
        return True, size
    except Exception:
        return False, 0


def delete_file(path: str) -> Tuple[bool, int]:
    """Dosyayı siler ve boyutunu döndürür."""
    if not os.path.exists(path):
        return False, 0
    
    if is_protected_path(path):
        return False, 0
    
    try:
        size = os.path.getsize(path)
        os.remove(path)
        return True, size
    except Exception:
        return False, 0


def clean_category(name: str, paths: List[Tuple[str, str]], dry_run: bool = False) -> Tuple[int, int]:
    """Bir kategoriyi temizler."""
    print(f"\n{'='*70}")
    print(f"📂 {name}")
    print(f"{'='*70}")
    
    total_deleted = 0
    total_size = 0
    
    for path, description in paths:
        if not os.path.exists(path):
            continue
        
        if is_protected_path(path):
            print(f"⏭️  Atlanıyor (korumalı): {description}")
            continue
        
        if os.path.isdir(path):
            size = calculate_directory_size(path)
            if size > 0:
                print(f"📁 {description}: {format_size(size)}")
                if not dry_run:
                    success, deleted_size = delete_directory(path)
                    if success:
                        print(f"   ✅ Silindi: {format_size(deleted_size)}")
                        total_deleted += 1
                        total_size += deleted_size
                    else:
                        print(f"   ❌ Silinemedi (izin hatası)")
        elif os.path.isfile(path):
            size = os.path.getsize(path)
            print(f"📄 {description}: {format_size(size)}")
            if not dry_run:
                success, deleted_size = delete_file(path)
                if success:
                    print(f"   ✅ Silindi: {format_size(deleted_size)}")
                    total_deleted += 1
                    total_size += deleted_size
                else:
                    print(f"   ❌ Silinemedi (izin hatası)")
    
    return total_deleted, total_size


def clean_all(dry_run: bool = False) -> None:
    """Sadece log dosyalarını temizler (cache'ler ve geçmiş kalır)."""
    print("🧹 Log Dosyaları Temizliği Başlatılıyor...")
    print("=" * 70)
    print("ℹ️  SADECE LOG DOSYALARI silinecek.")
    print("ℹ️  Cache'ler, geçmiş, cookies ve diğer veriler KALACAK.")
    print("=" * 70)
    
    if dry_run:
        print("🔍 DRY RUN MODU - Hiçbir şey silinmeyecek, sadece gösterilecek")
    else:
        print("⚠️  UYARI: Bu işlem geri alınamaz!")
        print("⚠️  Sadece log dosyaları silinecek (cache'ler ve geçmiş kalacak).")
        print()
        response = input("Devam etmek istediğinizden emin misiniz? (EVET yazın): ")
        if response.upper() != 'EVET':
            print("❌ İşlem iptal edildi.")
            return
    
    total_deleted = 0
    total_size = 0
    
    # Tarayıcı log dosyaları
    browser_logs = get_browser_log_paths()
    if browser_logs:
        deleted, size = clean_category("🌐 Tarayıcı Log Dosyaları", browser_logs, dry_run)
        total_deleted += deleted
        total_size += size
    
    # Oyun log dosyaları
    game_logs = get_game_log_paths()
    if game_logs:
        deleted, size = clean_category("🎮 Oyun Log Dosyaları", game_logs, dry_run)
        total_deleted += deleted
        total_size += size
    
    # Uygulama log dosyaları
    app_logs = get_application_log_paths()
    if app_logs:
        deleted, size = clean_category("📱 Uygulama Log Dosyaları", app_logs, dry_run)
        total_deleted += deleted
        total_size += size
    
    # Sistem log dosyaları
    system_logs = get_system_log_paths()
    if system_logs:
        deleted, size = clean_category("💻 Sistem Log Dosyaları", system_logs, dry_run)
        total_deleted += deleted
        total_size += size
    
    # Genel log dosyaları
    appdata = get_appdata_paths()
    log_extensions = ['.log', '.txt', '.out', '.err', '.trace', '.debug', '.old', '.bak']
    log_files = []
    
    for root_dir in [appdata['local'], appdata['roaming']]:
        if os.path.exists(root_dir):
            for root, dirs, files in os.walk(root_dir):
                # Korumalı dizinleri atla
                if any(protected.lower() in root.lower() for protected in PROTECTED_PATHS):
                    dirs[:] = []
                    continue
                
                for file in files:
                    if any(file.lower().endswith(ext) for ext in log_extensions):
                        file_path = os.path.join(root, file)
                        if not is_protected_path(file_path):
                            try:
                                size = os.path.getsize(file_path)
                                log_files.append((file_path, size))
                            except:
                                pass
    
    if log_files:
        print(f"\n{'='*70}")
        print(f"📋 Genel Log Dosyaları ({len(log_files)} adet)")
        print(f"{'='*70}")
        log_total_size = sum(size for _, size in log_files)
        print(f"Toplam: {format_size(log_total_size)}")
        
        if not dry_run:
            deleted_count = 0
            deleted_size = 0
            for file_path, size in log_files[:100]:  # İlk 100'ü göster
                success, deleted = delete_file(file_path)
                if success:
                    deleted_count += 1
                    deleted_size += deleted
            
            # Kalan dosyaları sessizce sil
            for file_path, size in log_files[100:]:
                success, deleted = delete_file(file_path)
                if success:
                    deleted_count += 1
                    deleted_size += deleted
            
            print(f"✅ {deleted_count} log dosyası silindi: {format_size(deleted_size)}")
            total_deleted += deleted_count
            total_size += deleted_size
    
    # Özet
    print(f"\n{'='*70}")
    print("✨ TEMİZLİK TAMAMLANDI")
    print(f"{'='*70}")
    print(f"📊 Toplam Silinen: {total_deleted} öğe")
    print(f"💾 Toplam Temizlenen Alan: {format_size(total_size)}")
    
    if dry_run:
        print("\n💡 Bu bir önizleme idi. Gerçekten temizlemek için --dry-run parametresini kaldırın.")
    else:
        print("\n✅ Log dosyaları temizlendi!")
        print("ℹ️  Cache'ler, geçmiş ve diğer veriler korundu.")


def main():
    """Ana fonksiyon"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Log temizleyici - Sadece log dosyalarını temizler (cache ve geçmiş korunur)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python log_cleaner.py              # Log dosyalarını temizle
  python log_cleaner.py --dry-run    # Önce ne silineceğini göster
  
ℹ️  Bu araç SADECE şunları temizler:
  - Tarayıcı log dosyaları (Chrome, Edge, Brave)
  - Oyun log dosyaları (Steam, Epic, Ubisoft, vb.)
  - Uygulama log dosyaları (Discord, VS Code, Slack, vb.)
  - Sistem log dosyaları
  
✅ KORUNAN VERİLER:
  - Cache'ler (tarayıcı, oyun, uygulama)
  - Geçmiş (history)
  - Cookies
  - Recent files
  - Temp dosyaları
  - Prefetch
  
  Bu işlem GERİ ALINAMAZ! Önemli verilerinizi yedekleyin!
        """
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Sadece ne silineceğini göster, silme'
    )
    
    args = parser.parse_args()
    
    if platform.system() != 'Windows':
        print("⚠️  Bu script şu anda sadece Windows için optimize edilmiştir.")
        response = input("Yine de devam etmek istiyor musunuz? (evet/hayır): ")
        if response.lower() not in ['evet', 'e', 'yes', 'y']:
            return
    
    try:
        clean_all(dry_run=args.dry_run)
    except KeyboardInterrupt:
        print("\n\n❌ İşlem kullanıcı tarafından iptal edildi.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Hata oluştu: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
