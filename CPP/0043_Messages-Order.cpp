// 18/10/2026
// Medium
// Debugging
// HackerRank: Implement the Factory design pattern and operator overloading to sort out-of-order network packets.

#include <iostream>
#include <algorithm>
#include <vector>
#include <string>

using namespace std;

class Message {
private:
    string text_;
    int id_;
public:
    Message() : text_(""), id_(0) {}
    Message(const string& text, int id) : text_(text), id_(id) {}
    
    const string& get_text() const {
        return text_;
    }
    
    bool operator<(const Message& other) const {
        return id_ < other.id_;
    }
};

class MessageFactory {
private:
    int current_id;
public:
    MessageFactory() : current_id(0) {}
    
    Message create_message(const string& text) {
        return Message(text, current_id++);
    }
};

class Recipient {
public:
    Recipient() {}
    void receive(const Message& msg) {
        messages_.push_back(msg);
    }
    void print_messages() {
        fix_order();
        for (auto& msg : messages_) {
            cout << msg.get_text() << endl;
        }
        messages_.clear();
    }
private:
    void fix_order() {
        sort(messages_.begin(), messages_.end());
    }
    vector<Message> messages_;
};

class Network {
public:
    static void send_messages(vector<Message> messages, Recipient& recipient) {
        reverse(messages.begin(), messages.end());
        for (auto msg : messages) {
            recipient.receive(msg);
        }
    }
};

int main() {
    MessageFactory message_factory;
    Recipient recipient;
    vector<Message> messages;
    string text;
    while (getline(cin, text)) {
        messages.push_back(message_factory.create_message(text));
    }
    Network::send_messages(messages, recipient);
    recipient.print_messages();
    
    return 0;
}