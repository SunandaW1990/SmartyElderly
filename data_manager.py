#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django 資料管理工具 v5.8
修正手動錄入的 ID 顯示問題，增加欄位格式提示，改進錯誤訊息
"""
import os
import sys
import csv
import json
from datetime import datetime
from django.core.exceptions import ValidationError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from django.apps import apps
from django.db import transaction
from django.core.paginator import Paginator

# ========== 通用清洗工具 ==========
def clean_string(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value if value != '' else None
    return value

def clean_int(value):
    if value is None or value == '':
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def clean_boolean(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ('true', '1', 'yes', 'y', '是'):
            return True
        if v in ('false', '0', 'no', 'n', '否'):
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    return None

def clean_datetime(value, fmt='%Y-%m-%d %H:%M:%S'):
    if value is None or value == '':
        return None
    if isinstance(value, datetime):
        return value
    for f in (fmt, '%Y-%m-%d', '%Y/%m/%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S'):
        try:
            return datetime.strptime(value, f)
        except ValueError:
            continue
    try:
        from dateutil.parser import parse
        return parse(value)
    except Exception:
        return None

# ========== 清洗規則 ==========
CLEAN_RULES = {
    'Course': {
        'title': (clean_string, True),
        'description': (clean_string, True),
        'comm_date': (clean_datetime, True),
        'district': (clean_string, True),
        'fee': (clean_int, True),
        'category': (clean_string, True),
        'course_url': (clean_string, False),
        'contact': (clean_string, True),
        'is_active': (clean_boolean, False),
        'creation_date': (clean_datetime, True),
        'poster_img': (clean_string, False),
    },
    # 可按需添加更多模型
}

# ========== 模型列表獲取 ==========
def get_all_models():
    models = []
    for model in apps.get_models():
        app_label = model._meta.app_label
        if app_label.startswith('django.') or app_label in ('taggit', 'auth', 'admin', 'contenttypes', 'sessions'):
            continue
        models.append(model)
    models.sort(key=lambda m: (m._meta.app_label, m.__name__))
    return models

def get_model_by_name(model_name):
    try:
        for model in apps.get_models():
            if model.__name__ == model_name:
                return model
    except:
        pass
    raise ValueError(f"找不到模型: {model_name}")

def get_model_fields(model_name, include_id=False):
    """獲取模型的所有欄位名稱，可選擇是否包含主鍵"""
    try:
        model = get_model_by_name(model_name)
        fields = []
        for f in model._meta.get_fields():
            # 跳過多對多、一對多
            if getattr(f, 'many_to_many', False):
                continue
            if getattr(f, 'one_to_many', False):
                continue
            # 如果是主鍵且不包含ID，跳過
            if f.primary_key and not include_id:
                continue
            # 跳過自動創建且不包含ID（但primary_key已處理，可省略）
            if f.auto_created and not include_id:
                continue
            fields.append(f.name)
        return fields
    except Exception as e:
        print(f"獲取欄位失敗: {e}")
        return []

def prompt_model_selection(prompt_text="請選擇模型"):
    models = get_all_models()
    if not models:
        print("目前項目中沒有可用的非內建模組。")
        return None

    print(f"\n{prompt_text}：")
    for idx, model in enumerate(models, 1):
        print(f"  {idx}. {model.__name__} (app: {model._meta.app_label})")
    print("  您也可以直接輸入模型名稱（大小寫敏感），或輸入 back/q 返回主選單")

    while True:
        user_input = input("請輸入編號或模型名稱: ").strip()
        if user_input.lower() in ('back', 'q'):
            return '##BACK##'
        if user_input.isdigit():
            num = int(user_input)
            if 1 <= num <= len(models):
                return models[num-1].__name__
            else:
                print(f"編號超出範圍，請輸入 1-{len(models)}")
                continue
        else:
            return user_input

def prompt_input(prompt, default=None, allow_back=True):
    if default is not None:
        prompt = f"{prompt}（直接回車使用預設: {default}）"
    if allow_back:
        prompt += "（輸入 back 或 q 返回主選單）"
    prompt += " "
    user_input = input(prompt).strip()
    if allow_back and user_input.lower() in ('back', 'q'):
        return '##BACK##'
    if user_input == '' and default is not None:
        return default
    return user_input

# ========== 智能檔案探測 ==========
def find_data_file(model_name, file_type='csv'):
    base = model_name.lower()
    candidates = [
        f"{base}.{file_type}",
        f"{base}s.{file_type}",
        f"{base}_data.{file_type}",
        f"{base}es.{file_type}",
        f"{base}s_data.{file_type}",
    ]
    candidates = list(dict.fromkeys(candidates))
    for cand in candidates:
        if os.path.exists(cand):
            return cand
    return None

# ========== 核心功能 ==========
def clean_row(row_dict, model_name):
    rules = CLEAN_RULES.get(model_name)
    if not rules:
        return {k: clean_string(v) for k, v in row_dict.items()}
    cleaned = {}
    for field, (func, required) in rules.items():
        raw = row_dict.get(field)
        value = func(raw) if func else raw
        if required and value is None:
            return None  # 必需欄位缺失或轉換失敗
        cleaned[field] = value
    return cleaned

def ask_user_for_action(row_num, errors):
    print(f"\n第 {row_num} 行數據驗證失敗，錯誤詳情：")
    for field, msgs in errors.items():
        print(f"  {field}: {', '.join(msgs)}")
    while True:
        choice = input("請選擇操作: (s)跳過該行  (a)終止匯入  (i)忽略所有後續錯誤: ").strip().lower()
        if choice in ('s', 'a', 'i'):
            return choice
        print("無效輸入，請輸入 s, a 或 i")

@transaction.atomic
def import_data(file_path, model_name, file_type='csv', batch_size=500, interactive=True):
    try:
        model = get_model_by_name(model_name)
    except ValueError as e:
        print(e)
        return

    try:
        if file_type == 'csv':
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        elif file_type == 'json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                rows = data if isinstance(data, list) else [data]
        else:
            print(f"不支援的檔案類型: {file_type}")
            return
    except FileNotFoundError:
        print(f"檔案不存在: {file_path}")
        return
    except Exception as e:
        print(f"讀取檔案出錯: {e}")
        return

    if not rows:
        print("檔案為空，沒有數據可匯入。")
        return

    print(f"共讀取 {len(rows)} 行數據，開始匯入...")
    objs = []
    total_imported = 0
    skip_all = False
    abort = False

    for idx, row in enumerate(rows, 1):
        if abort:
            break
        cleaned = clean_row(row, model_name)
        if cleaned is None:
            print(f"第 {idx} 行缺少必需欄位或格式不正確，跳過。")
            continue

        try:
            obj = model(**cleaned)
            obj.full_clean()
            objs.append(obj)
        except ValidationError as e:
            if not interactive or skip_all:
                print(f"第 {idx} 行驗證失敗，自動跳過（已忽略所有錯誤）")
                continue
            action = ask_user_for_action(idx, e.message_dict)
            if action == 's':
                continue
            elif action == 'a':
                abort = True
                print("終止匯入，已回滾所有更改。")
                break
            elif action == 'i':
                skip_all = True
                continue

        if len(objs) >= batch_size:
            model.objects.bulk_create(objs)
            total_imported += len(objs)
            objs = []
            print(f"已匯入 {total_imported} 條記錄...")

    if objs and not abort:
        model.objects.bulk_create(objs)
        total_imported += len(objs)

    if not abort:
        print(f"匯入完成！成功匯入 {total_imported} 條記錄到 {model_name}。")
    else:
        print("匯入已終止，未提交任何更改。")

def export_data(file_path, model_name, file_type='csv', queryset=None):
    try:
        model = get_model_by_name(model_name)
    except ValueError as e:
        print(e)
        return
    if queryset is None:
        queryset = model.objects.all()

    fields = [f.name for f in model._meta.get_fields() if not f.auto_created]
    fields = [f for f in fields if not getattr(model._meta.get_field(f), 'many_to_many', False)]

    data = []
    for obj in queryset:
        row = {}
        for field in fields:
            value = getattr(obj, field)
            if isinstance(value, datetime):
                value = value.isoformat()
            elif value is None:
                value = ''
            row[field] = value
        data.append(row)

    try:
        if file_type == 'csv':
            with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
                if data:
                    writer = csv.DictWriter(f, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(data)
            print(f"CSV 檔案已匯出: {file_path}，共 {len(data)} 條記錄。")
        elif file_type == 'json':
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"JSON 檔案已匯出: {file_path}，共 {len(data)} 條記錄。")
        else:
            print(f"不支援的匯出格式: {file_type}")
    except Exception as e:
        print(f"匯出失敗: {e}")

def clean_data_file(input_path, output_path, model_name, file_type='csv'):
    try:
        model = get_model_by_name(model_name)
    except ValueError as e:
        print(e)
        return

    try:
        if file_type == 'csv':
            with open(input_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        elif file_type == 'json':
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                rows = data if isinstance(data, list) else [data]
        else:
            print(f"不支援的檔案類型: {file_type}")
            return
    except Exception as e:
        print(f"讀取檔案出錯: {e}")
        return

    if not rows:
        print("檔案為空，無需清理。")
        return

    cleaned_rows = []
    for idx, row in enumerate(rows, 1):
        cleaned = clean_row(row, model_name)
        if cleaned is None:
            print(f"第 {idx} 行缺少必需欄位或格式不正確，已丟棄。")
            continue
        cleaned_rows.append(cleaned)

    if not cleaned_rows:
        print("清洗後沒有有效數據，不產生檔案。")
        return

    try:
        if file_type == 'csv':
            fieldnames = list(cleaned_rows[0].keys())
            with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(cleaned_rows)
            print(f"清洗後的 CSV 檔案已產生: {output_path}，共 {len(cleaned_rows)} 條記錄。")
        elif file_type == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(cleaned_rows, f, ensure_ascii=False, indent=2)
            print(f"清洗後的 JSON 檔案已產生: {output_path}，共 {len(cleaned_rows)} 條記錄。")
        else:
            print(f"不支援的輸出格式: {file_type}")
    except Exception as e:
        print(f"寫入檔案失敗: {e}")

def view_data(model_name, limit=20):
    try:
        model = get_model_by_name(model_name)
    except ValueError as e:
        print(e)
        return

    queryset = model.objects.all()
    total = queryset.count()
    if total == 0:
        print(f"模型 {model_name} 中沒有任何記錄。")
        return

    fields = [f.name for f in model._meta.get_fields() if not f.auto_created]
    fields = [f for f in fields if not getattr(model._meta.get_field(f), 'many_to_many', False)]

    paginator = Paginator(queryset, limit)
    page_num = 1
    while True:
        page = paginator.get_page(page_num)
        if not page:
            break
        print(f"\n=== {model_name} 記錄（第 {page_num} 頁，共 {paginator.num_pages} 頁）===")
        header = " | ".join(fields)
        print(header)
        print("-" * len(header))
        for obj in page:
            row = []
            for f in fields:
                val = getattr(obj, f)
                if isinstance(val, datetime):
                    val = val.strftime('%Y-%m-%d %H:%M')
                elif val is None:
                    val = ''
                row.append(str(val))
            print(" | ".join(row))
        print(f"共 {total} 條記錄，目前顯示第 {page.start_index()}-{page.end_index()} 條")
        if page_num >= paginator.num_pages:
            break
        next_action = input("輸入 'n' 查看下一頁，'q' 返回主選單: ").strip().lower()
        if next_action == 'q':
            break
        elif next_action == 'n':
            page_num += 1
        else:
            print("無效輸入，請輸入 n 或 q")
            continue

# ========== 手動錄入數據（修正版） ==========
def interactive_add_records():
    print("\n--- 手動錄入數據 ---")
    model_name = prompt_model_selection("請選擇要錄入數據的模型")
    if model_name == '##BACK##': return
    if not model_name:
        print("模型名稱不能為空。")
        return

    try:
        model = get_model_by_name(model_name)
        # 詢問是否包含 ID
        include_id = input("是否包含 ID 欄位（手動輸入）？(y/n，預設 n): ").strip().lower()
        include_id = (include_id == 'y')

        # 取得欄位
        fields = get_model_fields(model_name, include_id=include_id)
        if not fields:
            print("沒有可輸入的欄位。")
            return

        print(f"\n模型 {model_name} 的可用欄位：")
        for i, f in enumerate(fields, 1):
            # 給出格式提示
            hint = ""
            if 'date' in f.lower() or 'time' in f.lower():
                hint = " (格式: YYYY-MM-DD HH:MM:SS)"
            elif f.lower() == 'is_active' or 'bool' in f.lower():
                hint = " (接受 true/false, 1/0, yes/no)"
            print(f"  {i}. {f}{hint}")
        print("  （輸入 back 或 q 返回主選單，輸入 done 結束錄入）")

        records = []
        while True:
            print("\n--- 新增記錄（輸入欄位值，可直接回車跳過非必需欄位）---")
            row = {}
            for field in fields:
                val = input(f"  請輸入 {field}: ").strip()
                if val.lower() in ('back', 'q'):
                    print("操作已取消，返回主選單。")
                    return
                if val.lower() == 'done':
                    break
                row[field] = val
            if not row:
                break
            records.append(row)
            print(f"已新增記錄 #{len(records)}，繼續輸入下一筆...")

            cont = input("是否繼續新增下一筆？(y/n，預設 y): ").strip().lower()
            if cont == 'n':
                break

        if not records:
            print("沒有錄入任何數據。")
            return

        print(f"\n共錄入 {len(records)} 筆數據，即將儲存...")
        for i, row in enumerate(records, 1):
            print(f"  {i}. {row}")

        confirm = input("確認儲存？(y/n): ").strip().lower()
        if confirm != 'y':
            print("操作已取消。")
            return

        saved_count = 0
        for row in records:
            try:
                # 清洗
                cleaned = clean_row(row, model_name)
                if cleaned is None:
                    print(f"數據 {row} 缺少必需欄位或格式錯誤，跳過。")
                    continue
                # 若包含 ID，檢查是否存在
                if include_id and 'id' in cleaned and cleaned['id']:
                    existing = model.objects.filter(id=cleaned['id']).first()
                    if existing:
                        print(f"ID {cleaned['id']} 已存在，將更新該記錄。")
                        for key, value in cleaned.items():
                            setattr(existing, key, value)
                        existing.full_clean()
                        existing.save()
                        saved_count += 1
                    else:
                        obj = model(**cleaned)
                        obj.full_clean()
                        obj.save()
                        saved_count += 1
                else:
                    obj = model(**cleaned)
                    obj.full_clean()
                    obj.save()
                    saved_count += 1
            except ValidationError as e:
                print(f"驗證失敗，數據 {row} 未儲存：{e.message_dict}")
            except Exception as e:
                print(f"儲存失敗：{e}")

        print(f"成功儲存 {saved_count} 筆記錄到 {model_name}。")

    except Exception as e:
        print(f"發生錯誤：{e}")

# ========== 匯入（互動版） ==========
def interactive_import():
    print("\n--- 匯入資料 ---")
    model_name = prompt_model_selection("請選擇要匯入的目標模型")
    if model_name == '##BACK##': return
    if not model_name:
        print("模型名稱不能為空。")
        return

    found = find_data_file(model_name, 'csv')
    if found:
        file_path = found
        print(f"找到數據檔案: {file_path}")
    else:
        print(f"未找到預設數據檔案（嘗試了多種變體）")
        file_path = prompt_input("請手動輸入數據檔案路徑", default=None, allow_back=True)
        if file_path == '##BACK##': return
        if not file_path:
            print("檔案路徑不能為空。")
            return

    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
        print(f"\n檔案內容預覽（前5行）：")
        for i, line in enumerate(lines[:5], 1):
            print(f"{i}: {line.rstrip()}")
        if len(lines) > 5:
            print(f"... 共 {len(lines)} 行")
    except Exception as e:
        print(f"無法預覽檔案: {e}")

    try:
        model = get_model_by_name(model_name)
        count = model.objects.count()
        if count > 0:
            print(f"注意：模型 {model_name} 中已有 {count} 條記錄。")
            while True:
                choice = input("選擇操作: (a)追加數據  (o)覆蓋（清空全部再匯入） (c)取消: ").strip().lower()
                if choice == 'c':
                    print("操作已取消。")
                    return
                elif choice == 'o':
                    backup_choice = input("是否先備份現有數據？(y/n，預設 y): ").strip().lower()
                    if backup_choice != 'n':
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        backup_file = f"backup_{model_name}_{timestamp}.csv"
                        print(f"正在備份到 {backup_file} ...")
                        try:
                            export_data(backup_file, model_name, 'csv')
                            print("備份成功。")
                        except Exception as e:
                            print(f"備份失敗：{e}")
                            cont = input("備份失敗，是否仍然繼續清空？(y/n): ").strip().lower()
                            if cont != 'y':
                                print("操作已取消。")
                                return
                    print(f"正在清空 {model_name} 表（原有 {count} 條記錄）...")
                    try:
                        model.objects.all().delete()
                        print("清空成功。")
                    except Exception as e:
                        print(f"清空失敗：{e}")
                        print("可能因為其他表關聯到此表，請先處理關聯數據。")
                        return
                    break
                elif choice == 'a':
                    print("將保留現有數據，直接追加新數據。")
                    break
                else:
                    print("無效輸入，請輸入 a, o 或 c")
        else:
            print("目標表為空，將直接匯入。")
    except Exception as e:
        print(f"檢查數據時出錯: {e}")
        return

    confirm = input("確認執行匯入？(y/n): ").strip().lower()
    if confirm != 'y':
        print("匯入已取消。")
        return

    file_type = 'csv' if file_path.lower().endswith('.csv') else 'json'
    batch = 500
    print(f"\n開始匯入：檔案={file_path}, 模型={model_name}, 批量={batch}")
    import_data(file_path, model_name, file_type, batch, interactive=True)

# ========== 匯出（互動版） ==========
def interactive_export():
    print("\n--- 匯出資料 ---")
    model_name = prompt_model_selection("請選擇要匯出的模型")
    if model_name == '##BACK##': return
    if not model_name:
        print("模型名稱不能為空。")
        return

    default_file = f"export_{model_name.lower()}.csv"
    file_path = default_file
    file_type = 'csv'
    print(f"匯出檔案將儲存為: {file_path}")
    export_data(file_path, model_name, file_type)

# ========== 清理檔案（互動版） ==========
def interactive_clean_file():
    print("\n--- 清理並格式化資料檔案（不入庫） ---")
    model_name = prompt_model_selection("請選擇對應的模型（用於應用清洗規則）")
    if model_name == '##BACK##': return
    if not model_name:
        print("模型名稱不能為空。")
        return

    found = find_data_file(model_name, 'csv')
    if found:
        input_path = found
        print(f"找到輸入檔案: {input_path}")
    else:
        print(f"未找到預設數據檔案（嘗試了多種變體）")
        input_path = prompt_input("請手動輸入原始數據檔案路徑", default=None, allow_back=True)
        if input_path == '##BACK##': return
        if not input_path:
            print("檔案路徑不能為空。")
            return

    output_path = f"cleaned_{model_name.lower()}.csv"
    print(f"清理後的檔案將儲存為: {output_path}")

    file_type = 'csv' if input_path.lower().endswith('.csv') else 'json'
    print(f"\n開始清理：輸入={input_path}, 輸出={output_path}, 模型={model_name}")
    clean_data_file(input_path, output_path, model_name, file_type)

# ========== 查看數據（互動版） ==========
def interactive_view_data():
    print("\n--- 查看資料庫中的資料 ---")
    model_name = prompt_model_selection("請選擇要查看的模型")
    if model_name == '##BACK##': return
    if not model_name:
        print("模型名稱不能為空。")
        return
    limit = 20
    view_data(model_name, limit)

# ========== 刪除數據（互動版，含自動備份） ==========
def interactive_delete_data():
    print("\n--- 刪除指定模型的所有數據 ---")
    model_name = prompt_model_selection("請選擇要刪除的模型")
    if model_name == '##BACK##': return
    if not model_name:
        print("模型名稱不能為空。")
        return

    try:
        model = get_model_by_name(model_name)
        count = model.objects.count()
        if count == 0:
            print(f"模型 {model_name} 中沒有任何記錄，無需刪除。")
            return
        print(f"⚠️ 模型 {model_name} 中目前有 {count} 條記錄。")
        print("此操作將刪除全部記錄，且無法復原！")

        backup_choice = input("是否先備份現有數據？(y/n，預設 y): ").strip().lower()
        if backup_choice != 'n':
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = f"backup_{model_name}_{timestamp}.csv"
            print(f"正在備份到 {backup_file} ...")
            try:
                export_data(backup_file, model_name, 'csv')
                print("備份成功。")
            except Exception as e:
                print(f"備份失敗：{e}")
                cont = input("備份失敗，是否仍然繼續刪除？(y/n): ").strip().lower()
                if cont != 'y':
                    print("操作已取消。")
                    return

        confirm_name = input(f"請輸入模型名稱以確認刪除（輸入 '{model_name}' 繼續）: ").strip()
        if confirm_name != model_name:
            print("模型名稱輸入錯誤，操作已取消。")
            return

        confirm_yes = input("再次確認，輸入 'y' 執行刪除，其他任意鍵取消: ").strip().lower()
        if confirm_yes != 'y':
            print("操作已取消。")
            return

        try:
            with transaction.atomic():
                deleted, _ = model.objects.all().delete()
            print(f"成功刪除 {deleted} 條記錄。")
        except Exception as e:
            print(f"刪除失敗：{e}")
            print("可能因為其他表關聯到此表，請先處理關聯數據。")
    except Exception as e:
        print(f"發生錯誤：{e}")

# ========== 主選單 ==========
def main_menu():
    while True:
        print("\n" + "="*50)
        print("      Django 資料管理工具 v5.8")
        print("="*50)
        print("\n請選擇操作：")
        print("  1. 匯入資料（清洗 + 格式化 + 入庫）")
        print("  2. 匯出資料")
        print("  3. 清理並格式化資料檔案（不入庫）")
        print("  4. 查看資料庫中的資料")
        print("  5. 手動錄入資料（逐筆輸入，可選包含ID）")
        print("  6. 刪除指定模型的所有資料（含自動備份）")
        print("  7. 離開")
        choice = input("\n請輸入數字 (1-7): ").strip()

        if choice == '1':
            interactive_import()
        elif choice == '2':
            interactive_export()
        elif choice == '3':
            interactive_clean_file()
        elif choice == '4':
            interactive_view_data()
        elif choice == '5':
            interactive_add_records()
        elif choice == '6':
            interactive_delete_data()
        elif choice == '7':
            print("感謝使用，再見！")
            break
        else:
            print("無效輸入，請重新選擇。")
        input("\n按 Enter 鍵繼續...")

if __name__ == '__main__':
    main_menu()