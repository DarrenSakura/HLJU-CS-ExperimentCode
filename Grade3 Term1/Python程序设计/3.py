import json
import os

# 1. 设计Contact类封装联系人信息
class Contact:
    def __init__(self, name, phone, email=""):
        self.name = name
        self.phone = phone
        self.email = email

    # 转换为字典以便于 JSON 序列化
    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }

    # 从字典反序列化为 Contact 对象
    @classmethod
    def from_dict(cls, data):
        return cls(data.get("name"), data.get("phone"), data.get("email", ""))

# 2. 创建ContactManager类管理通讯录
class ContactManager:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    # 3. 实现JSON文件读写 (读操作)
    def load_contacts(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.contacts = [Contact.from_dict(item) for item in data]
            except Exception as e:
                print(f"读取通讯录文件失败: {e}")
        else:
            self.contacts = []

    # 3. 实现JSON文件读写 (写操作)
    def save_contacts(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                data = [contact.to_dict() for contact in self.contacts]
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存通讯录文件失败: {e}")

    # 4. 完成CRUD操作功能
    # 增 (Create)
    def add_contact(self, name, phone, email=""):
        for contact in self.contacts:
            if contact.name == name:
                print(f"联系人 '{name}' 已存在！")
                return False
        self.contacts.append(Contact(name, phone, email))
        self.save_contacts()
        print(f"成功添加联系人: {name}")
        return True

    # 删 (Delete)
    def delete_contact(self, name):
        for contact in self.contacts:
            if contact.name == name:
                self.contacts.remove(contact)
                self.save_contacts()
                print(f"成功删除联系人: {name}")
                return True
        print(f"未找到联系人: {name}")
        return False

    # 改 (Update)
    def update_contact(self, name, new_phone=None, new_email=None):
        for contact in self.contacts:
            if contact.name == name:
                if new_phone:
                    contact.phone = new_phone
                if new_email is not None:
                    contact.email = new_email
                self.save_contacts()
                print(f"成功更新联系人: {name} 的信息。")
                return True
        print(f"未找到联系人: {name}")
        return False

    # 查 (Read/Search)
    def search_contact(self, name):
        for contact in self.contacts:
            if contact.name == name:
                print(f"\n找到联系人 -> 姓名: {contact.name}, 电话: {contact.phone}, 邮箱: {contact.email}")
                return contact
        print(f"未找到联系人: {name}")
        return None

    # 显示所有联系人
    def list_contacts(self):
        if not self.contacts:
            print("\n当前通讯录为空。")
            return
        print("\n--- 所有联系人列表 ---")
        print(f"{'姓名':<15} | {'电话':<15} | {'邮箱'}")
        print("-" * 50)
        for contact in self.contacts:
            print(f"{contact.name:<15} | {contact.phone:<15} | {contact.email}")
        print("-" * 50)

# 5. 设计用户交互界面
def main():
    manager = ContactManager()
    
    while True:
        print("\n=== 通讯录管理系统 ===")
        print("1. 添加联系人 (Create)")
        print("2. 查找联系人 (Read)")
        print("3. 更新联系人 (Update)")
        print("4. 删除联系人 (Delete)")
        print("5. 显示所有联系人")
        print("6. 退出系统")
        
        choice = input("请选择操作 (1-6): ")
        
        if choice == '1':
            name = input("请输入姓名: ").strip()
            if not name:
                print("姓名不能为空！")
                continue
            phone = input("请输入电话: ").strip()
            email = input("请输入邮箱 (选填，直接回车��过): ").strip()
            manager.add_contact(name, phone, email)
            
        elif choice == '2':
            name = input("请输入要查找的联系人姓名: ").strip()
            manager.search_contact(name)
            
        elif choice == '3':
            name = input("请输入要更新的联系人姓名: ").strip()
            if manager.search_contact(name):
                print("请输入新信息 (直接回车表示不修改该项)：")
                new_phone = input("新电话: ").strip()
                new_email = input("新邮箱: ").strip()
                manager.update_contact(
                    name, 
                    new_phone if new_phone else None, 
                    new_email if new_email != "" else None
                )
                
        elif choice == '4':
            name = input("请输入要删除的联系人姓名: ").strip()
            # 二次确认
            confirm = input(f"确定要删除联系人 '{name}' 吗？(y/n): ")
            if confirm.lower() == 'y':
                manager.delete_contact(name)
            else:
                print("已取消删除。")
                
        elif choice == '5':
            manager.list_contacts()
            
        elif choice == '6':
            print("数据已自动保存。退出通讯录管理系统，再见！")
            break
            
        else:
            print("无效的选项，请重新输入 1-6 之间的数字。")

if __name__ == "__main__":
    main()