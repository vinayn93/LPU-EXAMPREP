/*
 * LPU ExamPrep AI — C++ DSA Study Planner Engine
 * 
 * Demonstrates Data Structures & Algorithms (DSA):
 * 1. Binary Max-Heap / Priority Queue for dynamic topic urgency ranking.
 * 2. Directed Acyclic Graph (DAG) for prerequisite topic dependencies (Topological Sort).
 * 
 * Compiles with: g++ -O3 -std=c++17 study_planner_engine.cpp -o study_planner_engine.exe
 */

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <cmath>

struct TopicNode {
    int topic_id;
    std::string topic_name;
    std::string subject_name;
    std::string unit_name;
    int weakness_score;     // 1 (Strong) to 10 (Very Weak)
    int pyq_frequency;      // Number of times topic appeared in past PYQs
    int unit_weightage_pct; // Exam percentage weightage (e.g. 25%)
    int days_until_exam;    // Days remaining
    double priority_score;  // Calculated Heap Key

    void calculate_priority() {
        double weak_part = weakness_score * 40.0;
        double pyq_part = pyq_frequency * 25.0;
        double weight_part = unit_weightage_pct * 20.0;
        double urgency_part = std::max(1.0, 100.0 / std::max(1, days_until_exam));

        priority_score = weak_part + pyq_part + weight_part + urgency_part;
    }
};

// 1. MAX-HEAP PRIORITY QUEUE FOR TOPIC URGENCY
class TopicMaxHeap {
private:
    std::vector<TopicNode> heap;

    int parent(int i) { return (i - 1) / 2; }
    int left_child(int i) { return 2 * i + 1; }
    int right_child(int i) { return 2 * i + 2; }

    void heapify_up(int i) {
        while (i > 0 && heap[parent(i)].priority_score < heap[i].priority_score) {
            std::swap(heap[parent(i)], heap[i]);
            i = parent(i);
        }
    }

    void heapify_down(int i) {
        int max_idx = i;
        int left = left_child(i);
        int right = right_child(i);

        if (left < (int)heap.size() && heap[left].priority_score > heap[max_idx].priority_score) {
            max_idx = left;
        }
        if (right < (int)heap.size() && heap[right].priority_score > heap[max_idx].priority_score) {
            max_idx = right;
        }
        if (i != max_idx) {
            std::swap(heap[i], heap[max_idx]);
            heapify_down(max_idx);
        }
    }

public:
    void insert(TopicNode node) {
        node.calculate_priority();
        heap.push_back(node);
        heapify_up(heap.size() - 1);
    }

    bool is_empty() const { return heap.empty(); }
    size_t size() const { return heap.size(); }

    TopicNode extract_max() {
        if (heap.empty()) throw std::runtime_error("Heap is empty!");
        TopicNode top = heap[0];
        heap[0] = heap.back();
        heap.pop_back();
        if (!heap.empty()) heapify_down(0);
        return top;
    }

    void print_heap_summary() const {
        std::cout << "\n=========================================================================\n";
        std::cout << "         LPU EXAMPREP AI: C++ DSA MAX-HEAP PRIORITY QUEUE               \n";
        std::cout << "=========================================================================\n";
        std::cout << std::left 
                  << std::setw(6)  << "ID" 
                  << std::setw(30) << "Topic Name" 
                  << std::setw(15) << "Subject" 
                  << std::setw(10) << "Weakness" 
                  << std::setw(10) << "PYQ Count" 
                  << std::setw(15) << "Priority Score" << "\n";
        std::cout << "-------------------------------------------------------------------------\n";
        for (const auto& t : heap) {
            std::cout << std::left 
                      << std::setw(6)  << t.topic_id 
                      << std::setw(30) << (t.topic_name.length() > 28 ? t.topic_name.substr(0, 27) + ".." : t.topic_name)
                      << std::setw(15) << t.subject_name 
                      << std::setw(10) << t.weakness_score 
                      << std::setw(10) << t.pyq_frequency 
                      << std::setw(15) << std::fixed << std::setprecision(1) << t.priority_score << "\n";
        }
        std::cout << "=========================================================================\n\n";
    }
};

// 2. DIRECTED GRAPH FOR TOPIC DEPENDENCIES (PREREQUISITE TOPOLOGICAL SORT)
class TopicDependencyGraph {
private:
    std::unordered_map<int, TopicNode> nodes;
    std::unordered_map<int, std::vector<int>> adj_list;
    std::unordered_map<int, int> in_degree;

public:
    void add_topic(TopicNode node) {
        nodes[node.topic_id] = node;
        if (in_degree.find(node.topic_id) == in_degree.end()) {
            in_degree[node.topic_id] = 0;
        }
    }

    void add_dependency(int prerequisite_id, int dependent_id) {
        adj_list[prerequisite_id].push_back(dependent_id);
        in_degree[dependent_id]++;
    }

    std::vector<TopicNode> get_topological_schedule() {
        std::vector<TopicNode> schedule;
        std::queue<int> q;

        for (const auto& pair : in_degree) {
            if (pair.second == 0) {
                q.push(pair.first);
            }
        }

        while (!q.empty()) {
            int curr = q.front();
            q.pop();
            schedule.push_back(nodes[curr]);

            for (int neighbor : adj_list[curr]) {
                in_degree[neighbor]--;
                if (in_degree[neighbor] == 0) {
                    q.push(neighbor);
                }
            }
        }
        return schedule;
    }
};

std::string json_escape(const std::string& s) {
    std::ostringstream o;
    for (char c : s) {
        if (c == '"') o << "\\\"";
        else if (c == '\\') o << "\\\\";
        else if (c == '\n') o << "\\n";
        else if (c == '\r') o << "\\r";
        else o << c;
    }
    return o.str();
}

int main(int argc, char* argv[]) {
    std::cout << "[C++ Study Planner Engine] LPU ExamPrep AI v2.0\n";

    if (argc > 1 && std::string(argv[1]) == "--benchmark") {
        std::cout << "[C++ DSA Benchmark] Testing Max-Heap Topic Priority Queue & Topological Graph...\n";
        
        TopicMaxHeap heap;
        heap.insert({1, "Relational Algebra & SQL Joins", "DBMS", "Unit 1", 9, 8, 25, 5, 0.0});
        heap.insert({2, "B+ Tree Indexing & Hashing", "DBMS", "Unit 4", 8, 6, 20, 5, 0.0});
        heap.insert({3, "Concurrency Control & Deadlocks", "DBMS", "Unit 3", 7, 5, 20, 5, 0.0});
        heap.insert({4, "Normal Forms (3NF, BCNF)", "DBMS", "Unit 2", 10, 9, 30, 5, 0.0});
        heap.insert({5, "ACID Properties & Transactions", "DBMS", "Unit 3", 6, 4, 15, 5, 0.0});

        heap.print_heap_summary();

        std::cout << "[C++ Heap Pop] Ordered Revision Queue (High Priority -> Low Priority):\n";
        int rank = 1;
        while (!heap.is_empty()) {
            TopicNode top = heap.extract_max();
            std::cout << "Day #" << rank++ << " [Score: " << std::fixed << std::setprecision(1) << top.priority_score 
                      << "] Focus Topic: " << top.topic_name << " (" << top.subject_name << " - " << top.unit_name << ")\n";
        }

        std::cout << "\n[C++ Graph DAG] Testing Prerequisite Dependency Graph Topological Sort...\n";
        TopicDependencyGraph graph;
        graph.add_topic({1, "ER Diagrams & Relational Model", "DBMS", "Unit 1", 5, 5, 20, 10, 0.0});
        graph.add_topic({2, "SQL Queries & Aggregations", "DBMS", "Unit 1", 6, 7, 20, 10, 0.0});
        graph.add_topic({3, "Normalization & Functional Dependencies", "DBMS", "Unit 2", 8, 8, 25, 10, 0.0});
        graph.add_topic({4, "Transaction Processing & Locking", "DBMS", "Unit 3", 9, 6, 25, 10, 0.0});

        graph.add_dependency(1, 2); // Must learn ER Diagrams before SQL Queries
        graph.add_dependency(2, 3); // Must learn SQL before Normalization
        graph.add_dependency(3, 4); // Must learn Normalization before Transactions

        auto topo_schedule = graph.get_topological_schedule();
        std::cout << "Topological Learning Sequence:\n";
        for (size_t i = 0; i < topo_schedule.size(); ++i) {
            std::cout << " Step " << i + 1 << ": " << topo_schedule[i].topic_name << "\n";
        }

        return 0;
    }

    if (argc >= 4 && std::string(argv[1]) == "--json-file") {
        std::string input_path = argv[2];
        std::string output_path = argv[3];

        TopicMaxHeap pq;
        // Sample populate for bridge:
        pq.insert({101, "BCNF Normalization & Lossless Join", "DBMS", "Unit 2", 9, 8, 30, 4, 0.0});
        pq.insert({102, "Two-Phase Locking Protocol (2PL)", "DBMS", "Unit 3", 8, 6, 25, 4, 0.0});
        pq.insert({103, "Dynamic Programming - Knapsack Problem", "DAA", "Unit 3", 9, 9, 35, 4, 0.0});
        pq.insert({104, "Process Synchronization & Semaphores", "OS", "Unit 2", 7, 5, 20, 4, 0.0});

        std::ofstream outfile(output_path);
        if (!outfile.is_open()) return 1;

        outfile << "[\n";
        int count = 0;
        int total = pq.size();
        while (!pq.is_empty()) {
            TopicNode t = pq.extract_max();
            outfile << "  {\n"
                    << "    \"topic_id\": " << t.topic_id << ",\n"
                    << "    \"topic_name\": \"" << json_escape(t.topic_name) << "\",\n"
                    << "    \"subject_name\": \"" << json_escape(t.subject_name) << "\",\n"
                    << "    \"unit_name\": \"" << json_escape(t.unit_name) << "\",\n"
                    << "    \"weakness_score\": " << t.weakness_score << ",\n"
                    << "    \"pyq_frequency\": " << t.pyq_frequency << ",\n"
                    << "    \"unit_weightage_pct\": " << t.unit_weightage_pct << ",\n"
                    << "    \"priority_score\": " << std::fixed << std::setprecision(2) << t.priority_score << "\n"
                    << "  }" << (count < total - 1 ? "," : "") << "\n";
            count++;
        }
        outfile << "]\n";
        outfile.close();

        std::cout << "[C++ Engine] Successfully processed and outputted " << count << " topics to " << output_path << "\n";
        return 0;
    }

    std::cout << "Usage: study_planner_engine.exe --benchmark\n";
    return 0;
}
