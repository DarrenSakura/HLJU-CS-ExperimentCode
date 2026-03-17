#include <iostream>
#include <vector>
#include <string>
#include <sstream>

using namespace std;

enum FileType { TYPE_DIR, TYPE_FILE, TYPE_FREE };

struct DirEntry {
    string name;
    int inum;
};

struct Inode {
    FileType type;
    int ref_count;
    vector<int> blocks;
    
    Inode() : type(TYPE_FREE), ref_count(0) {}
};

class VSFS {
private:
    int num_inodes;
    int num_data_blocks;
    
    vector<int> ibitmap;
    vector<int> dbitmap;
    vector<Inode> inodes;
    
    // 模拟数据块。目录存 DirEntry，文件存 dummy 数据（这里简单用整数标记使用情况）
    vector<vector<DirEntry>> dir_data_blocks; 
    
public:
    VSFS(int i_count, int d_count) : num_inodes(i_count), num_data_blocks(d_count) {
        ibitmap.assign(num_inodes, 0);
        dbitmap.assign(num_data_blocks, 0);
        inodes.resize(num_inodes);
        dir_data_blocks.resize(num_data_blocks);
        
        // 初始化根目录 /
        int root_inode = alloc_inode();
        int root_block = alloc_block();
        
        inodes[root_inode].type = TYPE_DIR;
        inodes[root_inode].ref_count = 2; // '.' 和 父目录指向它（根的父目录是自己）
        inodes[root_inode].blocks.push_back(root_block);
        
        dir_data_blocks[root_block].push_back({".", root_inode});
        dir_data_blocks[root_block].push_back({"..", root_inode});
    }
    
    int alloc_inode() {
        for (int i = 0; i < num_inodes; ++i) {
            if (ibitmap[i] == 0) {
                ibitmap[i] = 1;
                inodes[i] = Inode();
                return i;
            }
        }
        return -1;
    }
    
    int alloc_block() {
        for (int i = 0; i < num_data_blocks; ++i) {
            if (dbitmap[i] == 0) {
                dbitmap[i] = 1;
                dir_data_blocks[i].clear();
                return i;
            }
        }
        return -1;
    }
    
    void free_inode(int inum) {
        ibitmap[inum] = 0;
        inodes[inum].type = TYPE_FREE;
        inodes[inum].ref_count = 0;
        inodes[inum].blocks.clear();
    }
    
    void free_block(int bnum) {
        dbitmap[bnum] = 0;
        dir_data_blocks[bnum].clear();
    }
    
    // 解析路径，返回父目录的inode号和目标文件名
    bool parse_path(const string& path, int& parent_inum, string& target_name) {
        if (path == "/" || path.empty()) return false;
        
        int current_inum = 0; // root is 0
        int last_slash = path.find_last_of('/');
        string parent_path = path.substr(0, last_slash);
        target_name = path.substr(last_slash + 1);
        
        if (parent_path.empty()) parent_path = "/";
        
        // 简化版的路径解析，这里假设只能在根目录或一级子目录下操作
        // 对于完全支持多级目录，需要逐级切分解析
        if (parent_path == "/") {
            parent_inum = 0;
            return true;
        } else {
            string p_name = parent_path.substr(1);
            for (int b : inodes[0].blocks) {
                for (auto& entry : dir_data_blocks[b]) {
                    if (entry.name == p_name && inodes[entry.inum].type == TYPE_DIR) {
                        parent_inum = entry.inum;
                        return true;
                    }
                }
            }
        }
        return false;
    }
    
    int lookup(int parent_inum, const string& name) {
        for (int b : inodes[parent_inum].blocks) {
            for (auto& entry : dir_data_blocks[b]) {
                if (entry.name == name) return entry.inum;
            }
        }
        return -1;
    }

    void fs_mkdir(const string& path) {
        int pinum; string name;
        if (!parse_path(path, pinum, name)) return;
        
        int new_inum = alloc_inode();
        int new_bnum = alloc_block();
        
        inodes[new_inum].type = TYPE_DIR;
        inodes[new_inum].ref_count = 2; // '.' and parent
        inodes[new_inum].blocks.push_back(new_bnum);
        
        dir_data_blocks[new_bnum].push_back({".", new_inum});
        dir_data_blocks[new_bnum].push_back({"..", pinum});
        
        inodes[pinum].ref_count++;
        dir_data_blocks[inodes[pinum].blocks[0]].push_back({name, new_inum});
    }

    void fs_creat(const string& path) {
        int pinum; string name;
        if (!parse_path(path, pinum, name)) return;
        
        int new_inum = alloc_inode();
        inodes[new_inum].type = TYPE_FILE;
        inodes[new_inum].ref_count = 1;
        
        dir_data_blocks[inodes[pinum].blocks[0]].push_back({name, new_inum});
    }

    void fs_append(const string& path) {
        int pinum; string name;
        if (!parse_path(path, pinum, name)) return;
        
        int target_inum = lookup(pinum, name);
        if (target_inum != -1 && inodes[target_inum].type == TYPE_FILE) {
            int new_bnum = alloc_block();
            inodes[target_inum].blocks.push_back(new_bnum);
        }
    }

    void fs_link(const string& old_path, const string& new_path) {
        int old_pinum, new_pinum;
        string old_name, new_name;
        if (!parse_path(old_path, old_pinum, old_name) || !parse_path(new_path, new_pinum, new_name)) return;
        
        int target_inum = lookup(old_pinum, old_name);
        if (target_inum != -1) {
            inodes[target_inum].ref_count++;
            dir_data_blocks[inodes[new_pinum].blocks[0]].push_back({new_name, target_inum});
        }
    }

    void fs_unlink(const string& path) {
        int pinum; string name;
        if (!parse_path(path, pinum, name)) return;
        
        int target_inum = lookup(pinum, name);
        if (target_inum != -1) {
            // Remove from parent dir
            auto& entries = dir_data_blocks[inodes[pinum].blocks[0]];
            for (auto it = entries.begin(); it != entries.end(); ++it) {
                if (it->name == name) {
                    entries.erase(it);
                    break;
                }
            }
            
            inodes[target_inum].ref_count--;
            if (inodes[target_inum].ref_count == 0) {
                for (int b : inodes[target_inum].blocks) free_block(b);
                free_inode(target_inum);
            }
        }
    }

    void print_state() {
        cout << "inode bitmap: ";
        for (int b : ibitmap) cout << b;
        cout << "\ndata bitmap:  ";
        for (int b : dbitmap) cout << b;
        cout << "\n\ninodes:\n";
        
        for (int i = 0; i < num_inodes; ++i) {
            if (ibitmap[i]) {
                cout << "  [" << i << "] type:" << (inodes[i].type == TYPE_DIR ? "DIR " : "FILE")
                     << " ref:" << inodes[i].ref_count << " blocks:[";
                for (size_t j = 0; j < inodes[i].blocks.size(); ++j) {
                    cout << inodes[i].blocks[j] << (j == inodes[i].blocks.size()-1 ? "" : ",");
                }
                cout << "]\n";
            }
        }
        
        cout << "\ndata blocks:\n";
        for (int i = 0; i < num_data_blocks; ++i) {
            if (dbitmap[i]) {
                cout << "  [" << i << "] ";
                if (!dir_data_blocks[i].empty()) {
                    cout << "dir entries: ";
                    for (auto& e : dir_data_blocks[i]) cout << "(" << e.name << "," << e.inum << ") ";
                } else {
                    cout << "file data...";
                }
                cout << "\n";
            }
        }
        cout << "--------------------------------------\n";
    }
};

int main() {
    int inodes_count, blocks_count;
    cout << "输入 inodes 的数量和数据块的数量 (如 8 16): ";
    if (!(cin >> inodes_count >> blocks_count)) return 0;

    VSFS fs(inodes_count, blocks_count);
    
    cout << "\n[Initial State]\n";
    fs.print_state();

    cout << "\n>>> mkdir(\"/a\")\n";
    fs.fs_mkdir("/a");
    fs.print_state();

    cout << "\n>>> creat(\"/a/b\")\n";
    fs.fs_creat("/a/b");
    fs.print_state();

    cout << "\n>>> open+write+close(\"/a/b\")  -> append block\n";
    fs.fs_append("/a/b");
    fs.print_state();

    cout << "\n>>> link(\"/a/b\", \"/c\")\n";
    fs.fs_link("/a/b", "/c");
    fs.print_state();

    cout << "\n>>> unlink(\"/a/b\")\n";
    fs.fs_unlink("/a/b");
    fs.print_state();

    return 0;
}