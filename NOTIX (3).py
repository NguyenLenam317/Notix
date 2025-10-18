import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import json
import os


class StudentManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Notix")
        self.root.geometry("800x600")

        # Khởi tạo dữ liệu
        self.load_data()

        # Hiển thị menu chính
        self.show_main_menu()

    def load_data(self):
        if not os.path.exists('data.json'):
            self.data = {
                'schedule': {},
                'homework': [],
                'tasks': [],
                'progress': {}
            }
            self.save_data()
        else:
            with open('data.json', 'r', encoding='utf-8') as f:
                self.data = json.load(f)

    def save_data(self):
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_window()

        # Tạo frame cho menu chính
        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(expand=True)

        ttk.Label(menu_frame, text="MENU", font=('Helvetica', 16, 'bold')).pack(pady=20)

        # Các nút menu
        ttk.Button(menu_frame, text="1. Thời Khóa Biểu",
                   command=lambda: self.setup_schedule_tab()).pack(pady=10, padx=20, fill='x')
        ttk.Button(menu_frame, text="2. Quản Lý Bài Tập",
                   command=lambda: self.setup_homework_tab()).pack(pady=10, padx=20, fill='x')
        ttk.Button(menu_frame, text="3. Quản Lý Công Việc",
                   command=lambda: self.setup_task_tab()).pack(pady=10, padx=20, fill='x')
        ttk.Button(menu_frame, text="4. Tiến Độ Học Tập",
                   command=lambda: self.setup_progress_tab()).pack(pady=10, padx=20, fill='x')
        ttk.Button(menu_frame, text="Thoát",
                   command=self.root.quit).pack(pady=20, padx=20, fill='x')

    def setup_schedule_tab(self):
        self.clear_window()

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)

        # Frame cho input
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(pady=10)

        # Input fields
        ttk.Label(input_frame, text="Môn học:").grid(row=0, column=0, padx=5)
        self.subject_entry = ttk.Entry(input_frame)
        self.subject_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Tiết:").grid(row=0, column=2, padx=5)
        self.period_entry = ttk.Entry(input_frame)
        self.period_entry.grid(row=0, column=3, padx=5)

        ttk.Label(input_frame, text="Thứ:").grid(row=0, column=4, padx=5)
        self.day_combo = ttk.Combobox(input_frame,
                                      values=['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật'])
        self.day_combo.grid(row=0, column=5, padx=5)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="Thêm", command=self.add_schedule).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Sửa", command=self.edit_schedule).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.delete_schedule).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Quay lại Menu",
                   command=self.show_main_menu).pack(side='left', padx=5)

        # Treeview
        self.schedule_tree = ttk.Treeview(main_frame, columns=(
        'Tiết', 'Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật'))
        self.schedule_tree.heading('Tiết', text='Tiết')
        self.schedule_tree.heading('Thứ 2', text='Thứ 2')
        self.schedule_tree.heading('Thứ 3', text='Thứ 3')
        self.schedule_tree.heading('Thứ 4', text='Thứ 4')
        self.schedule_tree.heading('Thứ 5', text='Thứ 5')
        self.schedule_tree.heading('Thứ 6', text='Thứ 6')
        self.schedule_tree.heading('Thứ 7', text='Thứ 7')
        self.schedule_tree.heading('Chủ nhật', text='Chủ nhật')
        self.schedule_tree.pack(pady=10, fill='both', expand=True)

        self.update_schedule_display()

    def setup_homework_tab(self):
        self.clear_window()

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)

        # Frame cho input
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Bài tập:").grid(row=0, column=0, padx=5)
        self.homework_entry = ttk.Entry(input_frame)
        self.homework_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Hạn nộp:").grid(row=0, column=2, padx=5)
        self.homework_deadline = ttk.Entry(input_frame)
        self.homework_deadline.grid(row=0, column=3, padx=5)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="Thêm", command=self.add_homework).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Sửa", command=self.edit_homework).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.delete_homework).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Đánh dấu hoàn thành",
                   command=self.mark_homework_complete).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Quay lại Menu",
                   command=self.show_main_menu).pack(side='left', padx=5)

        # Treeview
        self.homework_tree = ttk.Treeview(main_frame, columns=('Bài tập', 'Hạn nộp', 'Trạng thái'))
        self.homework_tree.heading('Bài tập', text='Bài tập')
        self.homework_tree.heading('Hạn nộp', text='Hạn nộp')
        self.homework_tree.heading('Trạng thái', text='Trạng thái')
        self.homework_tree.pack(pady=10, fill='both', expand=True)

        self.update_homework_display()

    def setup_task_tab(self):
        self.clear_window()

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)

        # Frame cho input
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Tên công việc:").grid(row=0, column=0, padx=5)
        self.task_name_entry = ttk.Entry(input_frame)
        self.task_name_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Mô tả:").grid(row=0, column=2, padx=5)
        self.task_desc_entry = ttk.Entry(input_frame)
        self.task_desc_entry.grid(row=0, column=3, padx=5)

        ttk.Label(input_frame, text="Hạn:").grid(row=0, column=4, padx=5)
        self.task_deadline = ttk.Entry(input_frame)
        self.task_deadline.grid(row=0, column=5, padx=5)

        ttk.Label(input_frame, text="Ưu tiên:").grid(row=0, column=6, padx=5)
        self.priority_combo = ttk.Combobox(input_frame, values=['Cao', 'Trung bình', 'Thấp'])
        self.priority_combo.grid(row=0, column=7, padx=5)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="Thêm", command=self.add_task).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Sửa", command=self.edit_task).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.delete_task).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Quay lại Menu",
                   command=self.show_main_menu).pack(side='left', padx=5)

        # Filter frame
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(pady=5)

        ttk.Label(filter_frame, text="Lọc theo ưu tiên:").pack(side='left', padx=5)
        self.priority_filter = ttk.Combobox(filter_frame, values=['Tất cả', 'Cao', 'Trung bình', 'Thấp'])
        self.priority_filter.pack(side='left', padx=5)
        self.priority_filter.set('Tất cả')
        self.priority_filter.bind('<<ComboboxSelected>>', self.filter_tasks)

        # Treeview
        self.task_tree = ttk.Treeview(main_frame, columns=('Tên', 'Mô tả', 'Hạn', 'Ưu tiên'))
        self.task_tree.heading('Tên', text='Tên')
        self.task_tree.heading('Mô tả', text='Mô tả')
        self.task_tree.heading('Hạn', text='Hạn')
        self.task_tree.heading('Ưu tiên', text='Ưu tiên')
        self.task_tree.pack(pady=10, fill='both', expand=True)

        self.update_task_display()

    def setup_progress_tab(self):
        self.clear_window()

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)

        # Frame cho input
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Môn học:").grid(row=0, column=0, padx=5)
        self.subject_progress_combo = ttk.Combobox(input_frame,
                                                   values=['Toán', 'Văn', 'Anh', 'Lý', 'Hóa', 'Sử', 'Địa'])
        self.subject_progress_combo.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Điểm:").grid(row=0, column=2, padx=5)
        self.score_entry = ttk.Entry(input_frame)
        self.score_entry.grid(row=0, column=3, padx=5)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="Thêm", command=self.add_score).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Sửa", command=self.edit_score).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.delete_score).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Quay lại Menu",
                   command=self.show_main_menu).pack(side='left', padx=5)

        # Treeview
        self.progress_tree = ttk.Treeview(main_frame, columns=('Môn học', 'Điểm', 'Trung bình'))
        self.progress_tree.heading('Môn học', text='Môn học')
        self.progress_tree.heading('Điểm', text='Điểm')
        self.progress_tree.heading('Trung bình', text='Trung bình')
        self.progress_tree.pack(pady=10, fill='both', expand=True)

        self.update_progress_display()

    # Các hàm chỉnh sửa dữ liệu
    def edit_schedule(self):
        selected_item = self.schedule_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mục để sửa")
            return

        item = self.schedule_tree.item(selected_item[0])
        period = item['values'][0]

        # Hiển thị dialog chỉnh sửa
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Sửa Thời Khóa Biểu")

        ttk.Label(edit_window, text="Chọn ngày:").pack()
        day_combo = ttk.Combobox(edit_window, values=['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật'])
        day_combo.pack()

        ttk.Label(edit_window, text="Môn học mới:").pack()
        new_subject = ttk.Entry(edit_window)
        new_subject.pack()

        def save_changes():
            day = day_combo.get()
            subject = new_subject.get()
            if day and subject:
                key = f"{day}-{period}"
                self.data['schedule'][key] = subject
                self.save_data()
                self.update_schedule_display()
                edit_window.destroy()

        ttk.Button(edit_window, text="Lưu", command=save_changes).pack()

    def delete_schedule(self):
        selected_item = self.schedule_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mục để xóa")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa mục này?"):
            item = self.schedule_tree.item(selected_item[0])
            period = item['values'][0]

            # Xóa tất cả các môn học trong tiết này
            keys_to_delete = []
            for key in self.data['schedule'].keys():
                if key.endswith(f"-{period}"):
                    keys_to_delete.append(key)

            for key in keys_to_delete:
                del self.data['schedule'][key]

            self.save_data()
            self.update_schedule_display()

    def edit_homework(self):
        selected_item = self.homework_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một bài tập để sửa")
            return

        item = self.homework_tree.item(selected_item[0])
        homework_name = item['values'][0]

        # Tìm bài tập trong data
        homework_index = None
        for i, hw in enumerate(self.data['homework']):
            if hw['homework'] == homework_name:
                homework_index = i
                break

        if homework_index is not None:
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Sửa Bài Tập")

            ttk.Label(edit_window, text="Tên bài tập:").pack()
            new_name = ttk.Entry(edit_window)
            new_name.insert(0, self.data['homework'][homework_index]['homework'])
            new_name.pack()

            ttk.Label(edit_window, text="Hạn nộp:").pack()
            new_deadline = ttk.Entry(edit_window)
            new_deadline.insert(0, self.data['homework'][homework_index]['deadline'])
            new_deadline.pack()

            def save_changes():
                self.data['homework'][homework_index]['homework'] = new_name.get()
                self.data['homework'][homework_index]['deadline'] = new_deadline.get()
                self.save_data()
                self.update_homework_display()
                edit_window.destroy()

            ttk.Button(edit_window, text="Lưu", command=save_changes).pack()

    def delete_homework(self):
        selected_item = self.homework_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một bài tập để xóa")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa bài tập này?"):
            item = self.homework_tree.item(selected_item[0])
            homework_name = item['values'][0]

            self.data['homework'] = [hw for hw in self.data['homework']
                                     if hw['homework'] != homework_name]
            self.save_data()
            self.update_homework_display()

    def edit_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một công việc để sửa")
            return

        item = self.task_tree.item(selected_item[0])
        task_name = item['values'][0]

        # Tìm công việc trong data
        task_index = None
        for i, task in enumerate(self.data['tasks']):
            if task['name'] == task_name:
                task_index = i
                break

        if task_index is not None:
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Sửa Công Việc")

            ttk.Label(edit_window, text="Tên công việc:").pack()
            new_name = ttk.Entry(edit_window)
            new_name.insert(0, self.data['tasks'][task_index]['name'])
            new_name.pack()

            ttk.Label(edit_window, text="Mô tả:").pack()
            new_desc = ttk.Entry(edit_window)
            new_desc.insert(0, self.data['tasks'][task_index]['description'])
            new_desc.pack()

            ttk.Label(edit_window, text="Hạn:").pack()
            new_deadline = ttk.Entry(edit_window)
            new_deadline.insert(0, self.data['tasks'][task_index]['deadline'])
            new_deadline.pack()

            ttk.Label(edit_window, text="Ưu tiên:").pack()
            new_priority = ttk.Combobox(edit_window, values=['Cao', 'Trung bình', 'Thấp'])
            new_priority.set(self.data['tasks'][task_index]['priority'])
            new_priority.pack()

            def save_changes():
                self.data['tasks'][task_index]['name'] = new_name.get()
                self.data['tasks'][task_index]['description'] = new_desc.get()
                self.data['tasks'][task_index]['deadline'] = new_deadline.get()
                self.data['tasks'][task_index]['priority'] = new_priority.get()
                self.save_data()
                self.update_task_display()
                edit_window.destroy()

            ttk.Button(edit_window, text="Lưu", command=save_changes).pack()

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một công việc để xóa")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa công việc này?"):
            item = self.task_tree.item(selected_item[0])
            task_name = item['values'][0]

            self.data['tasks'] = [task for task in self.data['tasks']
                                  if task['name'] != task_name]
            self.save_data()
            self.update_task_display()

    def edit_score(self):
        selected_item = self.progress_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một môn học để sửa")
            return

        item = self.progress_tree.item(selected_item[0])
        subject = item['values'][0]
        scores = self.data['progress'].get(subject, [])

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Sửa Điểm")

        ttk.Label(edit_window, text="Điểm số (phân cách bằng dấu phẩy):").pack()
        scores_entry = ttk.Entry(edit_window)
        scores_entry.insert(0, ", ".join(map(str, scores)))
        scores_entry.pack()

        def save_changes():
            try:
                new_scores = [float(x.strip()) for x in scores_entry.get().split(",")]
                if all(0 <= score <= 10 for score in new_scores):
                    self.data['progress'][subject] = new_scores
                    self.save_data()
                    self.update_progress_display()
                    edit_window.destroy()
                else:
                    messagebox.showwarning("Lỗi", "Điểm số phải từ 0 đến 10")
            except ValueError:
                messagebox.showwarning("Lỗi", "Vui lòng nhập điểm số hợp lệ")

        ttk.Button(edit_window, text="Lưu", command=save_changes).pack()

    def delete_score(self):
        selected_item = self.progress_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một môn học để xóa")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa điểm của môn học này?"):
            item = self.progress_tree.item(selected_item[0])
            subject = item['values'][0]

            if subject in self.data['progress']:
                del self.data['progress'][subject]
                self.save_data()
                self.update_progress_display()

    # Các hàm hiển thị và cập nhật giao diện (giữ nguyên như cũ)
    def update_schedule_display(self):
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)

        schedule_matrix = {str(i): [''] * 7 for i in range(1, 11)}

        for key, subject in self.data['schedule'].items():
            day, period = key.split('-')
            day_index = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật'].index(day)
            schedule_matrix[period][day_index] = subject

        for period in range(1, 11):
            values = schedule_matrix[str(period)]
            self.schedule_tree.insert('', 'end', values=(period,) + tuple(values))

    def update_homework_display(self):
        for item in self.homework_tree.get_children():
            self.homework_tree.delete(item)

        for homework in self.data['homework']:
            status = "Hoàn thành" if homework['completed'] else "Chưa hoàn thành"
            self.homework_tree.insert('', 'end', values=(homework['homework'],
                                                         homework['deadline'],
                                                         status))

    def update_task_display(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        priority_filter = self.priority_filter.get()

        for task in self.data['tasks']:
            if priority_filter == 'Tất cả' or task['priority'] == priority_filter:
                self.task_tree.insert('', 'end', values=(task['name'],
                                                         task['description'],
                                                         task['deadline'],
                                                         task['priority']))

    def update_progress_display(self):
        for item in self.progress_tree.get_children():
            self.progress_tree.delete(item)

        for subject, scores in self.data['progress'].items():
            if scores:
                average = sum(scores) / len(scores)
                self.progress_tree.insert('', 'end', values=(subject,
                                                             ', '.join(map(str, scores)),
                                                             f"{average:.2f}"))

    def filter_tasks(self, event=None):
        self.update_task_display()

    def mark_homework_complete(self):
        selected_item = self.homework_tree.selection()
        if selected_item:
            item = self.homework_tree.item(selected_item[0])
            homework_name = item['values'][0]

            for homework in self.data['homework']:
                if homework['homework'] == homework_name:
                    homework['completed'] = True
                    break

            self.save_data()
            self.update_homework_display()

    def add_schedule(self):
        subject = self.subject_entry.get()
        period = self.period_entry.get()
        day = self.day_combo.get()

        if subject and period and day:
            key = f"{day}-{period}"
            self.data['schedule'][key] = subject
            self.save_data()
            self.update_schedule_display()

            self.subject_entry.delete(0, tk.END)
            self.period_entry.delete(0, tk.END)
            self.day_combo.set('')

    def add_homework(self):
        homework = self.homework_entry.get()
        deadline = self.homework_deadline.get()

        if homework and deadline:
            self.data['homework'].append({
                'homework': homework,
                'deadline': deadline,
                'completed': False
            })
            self.save_data()
            self.update_homework_display()

            self.homework_entry.delete(0, tk.END)
            self.homework_deadline.delete(0, tk.END)

    def add_task(self):
        name = self.task_name_entry.get()
        desc = self.task_desc_entry.get()
        deadline = self.task_deadline.get()
        priority = self.priority_combo.get()

        if name and deadline and priority:
            self.data['tasks'].append({
                'name': name,
                'description': desc,
                'deadline': deadline,
                'priority': priority
            })
            self.save_data()
            self.update_task_display()

            self.task_name_entry.delete(0, tk.END)
            self.task_desc_entry.delete(0, tk.END)
            self.task_deadline.delete(0, tk.END)
            self.priority_combo.set('')

    def add_score(self):
        subject = self.subject_progress_combo.get()
        score = self.score_entry.get()

        if subject and score:
            if subject not in self.data['progress']:
                self.data['progress'][subject] = []
            try:
                score_float = float(score)
                if 0 <= score_float <= 10:
                    self.data['progress'][subject].append(score_float)
                    self.save_data()
                    self.update_progress_display()

                    self.subject_progress_combo.set('')
                    self.score_entry.delete(0, tk.END)
            except ValueError:
                pass

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = StudentManager()
    app.run()