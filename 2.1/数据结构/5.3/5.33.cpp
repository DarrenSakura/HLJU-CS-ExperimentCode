#include <iostream>
#include <stack>

using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

void preorderTraversal(TreeNode* root) {
    stack<TreeNode*> nodeStack;
    while (root != nullptr || !nodeStack.empty()) {
        while (root != nullptr) {
            cout << root->val << " ";
            nodeStack.push(root);
            root = root->left;
        }
        root = nodeStack.top();
        nodeStack.pop();
        root = root->right;
    }
}
void inorderTraversal(TreeNode* root) {
    stack<TreeNode*> nodeStack;
    TreeNode* curr = root;
    while (curr != nullptr || !nodeStack.empty()) {
        while (curr != nullptr) {
            nodeStack.push(curr);
            curr = curr->left;
        }
        curr = nodeStack.top();
        nodeStack.pop();
        cout << curr->val << " ";
        curr = curr->right;
    }
}

void postorderTraversal(TreeNode* root) {
    if (root == nullptr) {
        return;
    }
    stack<TreeNode*> leftNodeStack;
    stack<TreeNode*> rightNodeStack;
    leftNodeStack.push(root);
    while (!leftNodeStack.empty()) {
        TreeNode* node = leftNodeStack.top();
        leftNodeStack.pop();
        rightNodeStack.push(node);
        if (node->left != nullptr) {
            leftNodeStack.push(node->left);
        }
        if (node->right != nullptr) {
            leftNodeStack.push(node->right);
        }
    }
    while (!rightNodeStack.empty()) {
        cout << rightNodeStack.top()->val << " ";
        rightNodeStack.pop();
    }
}
int main() {
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);
    root->right->left = new TreeNode(6);
    root->right->right = new TreeNode(7);

    cout << "Preorder traversal: ";
    preorderTraversal(root);
    cout << endl;

    cout << "Inorder traversal: ";
    inorderTraversal(root);
    cout << endl;

    cout << "Postorder traversal: ";
    postorderTraversal(root);
    cout << endl;

    return 0;
}
