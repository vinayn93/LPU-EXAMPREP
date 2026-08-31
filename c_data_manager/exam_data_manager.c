/*
 * LPU ExamPrep AI — C Academic Data Manager Utility
 * Demonstrates C pointers, structures, linked lists, quicksort, and CSV file I/O.
 * 
 * Compiles with: gcc -O2 exam_data_manager.c -o exam_data_manager.exe
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_RECORDS 500
#define STR_LEN 256

typedef struct {
    int id;
    char subject[64];
    char unit[64];
    char question_text[STR_LEN];
    int marks;
    int year;
    char difficulty[16]; // Easy, Medium, Hard
} QuestionRecord;

// Node for Linked List demonstration
typedef struct QuestionNode {
    QuestionRecord data;
    struct QuestionNode* next;
} QuestionNode;

QuestionRecord dataset[MAX_RECORDS];
int total_questions = 0;

// Compare function for Quicksort by Year (Descending)
int compare_year_desc(const void* a, const void* b) {
    QuestionRecord* q1 = (QuestionRecord*)a;
    QuestionRecord* q2 = (QuestionRecord*)b;
    return q2->year - q1->year;
}

// Compare function for Quicksort by Marks (Descending)
int compare_marks_desc(const void* a, const void* b) {
    QuestionRecord* q1 = (QuestionRecord*)a;
    QuestionRecord* q2 = (QuestionRecord*)b;
    return q2->marks - q1->marks;
}

void print_question_records(QuestionRecord records[], int count) {
    printf("\n========================================================================================\n");
    printf("                  C DATA MANAGER: LPU ACADEMIC QUESTION BANK RECORDS                    \n");
    printf("========================================================================================\n");
    printf("%-5s | %-12s | %-10s | %-38s | %-5s | %-5s | %-8s\n", "ID", "Subject", "Unit", "Question Snippet", "Marks", "Year", "Level");
    printf("----------------------------------------------------------------------------------------\n");

    for (int i = 0; i < count; i++) {
        char text_snippet[36];
        if (strlen(records[i].question_text) > 33) {
            strncpy(text_snippet, records[i].question_text, 30);
            text_snippet[30] = '\0';
            strcat(text_snippet, "...");
        } else {
            strcpy(text_snippet, records[i].question_text);
        }

        printf("%-5d | %-12s | %-10s | %-38s | %-5d | %-5d | %-8s\n",
               records[i].id,
               records[i].subject,
               records[i].unit,
               text_snippet,
               records[i].marks,
               records[i].year,
               records[i].difficulty);
    }
    printf("========================================================================================\n");
    printf("Total records: %d\n\n", count);
}

void load_sample_questions() {
    total_questions = 6;
    dataset[0] = (QuestionRecord){1001, "DBMS", "Unit 2", "Explain 3NF vs BCNF normalization with examples.", 10, 2024, "Hard"};
    dataset[1] = (QuestionRecord){1002, "DBMS", "Unit 1", "Define primary key, foreign key, and candidate key.", 5, 2023, "Easy"};
    dataset[2] = (QuestionRecord){1003, "DAA", "Unit 3", "Solve 0/1 Knapsack Problem using Dynamic Programming.", 12, 2024, "Hard"};
    dataset[3] = (QuestionRecord){1004, "OS", "Unit 2", "Explain Peterson's Algorithm for Mutual Exclusion.", 8, 2022, "Medium"};
    dataset[4] = (QuestionRecord){1005, "CN", "Unit 4", "Differentiate between IPv4 and IPv6 packet headers.", 5, 2024, "Easy"};
    dataset[5] = (QuestionRecord){1006, "DBMS", "Unit 3", "Describe 2-Phase Locking Protocol and Deadlock Prevention.", 10, 2023, "Medium"};
}

void export_to_csv(const char* filename, QuestionRecord records[], int count) {
    FILE* fp = fopen(filename, "w");
    if (!fp) {
        printf("[C CLI Error] Cannot open %s for writing.\n", filename);
        return;
    }
    fprintf(fp, "ID,Subject,Unit,QuestionText,Marks,Year,Difficulty\n");
    for (int i = 0; i < count; i++) {
        fprintf(fp, "%d,\"%s\",\"%s\",\"%s\",%d,%d,\"%s\"\n",
                records[i].id, records[i].subject, records[i].unit,
                records[i].question_text, records[i].marks, records[i].year, records[i].difficulty);
    }
    fclose(fp);
    printf("[C CLI Success] Exported %d records to CSV file: %s\n", count, filename);
}

void search_questions(const char* keyword) {
    printf("[C Search Engine] Searching questions for keyword '%s'...\n", keyword);
    QuestionRecord results[MAX_RECORDS];
    int res_count = 0;

    for (int i = 0; i < total_questions; i++) {
        if (strstr(dataset[i].subject, keyword) != NULL ||
            strstr(dataset[i].unit, keyword) != NULL ||
            strstr(dataset[i].question_text, keyword) != NULL ||
            strstr(dataset[i].difficulty, keyword) != NULL) {
            results[res_count++] = dataset[i];
        }
    }
    print_question_records(results, res_count);
}

int main(int argc, char* argv[]) {
    printf("[C Academic Data Manager] LPU ExamPrep Question Bank Utility\n");
    load_sample_questions();

    if (argc > 1 && strcmp(argv[1], "--benchmark") == 0) {
        printf("\n--- Initial Unsorted Question Records ---\n");
        print_question_records(dataset, total_questions);

        printf("\n--- Quicksort by Year (Recent First) ---\n");
        qsort(dataset, total_questions, sizeof(QuestionRecord), compare_year_desc);
        print_question_records(dataset, total_questions);

        printf("\n--- Quicksort by Marks (Highest Weightage First) ---\n");
        qsort(dataset, total_questions, sizeof(QuestionRecord), compare_marks_desc);
        print_question_records(dataset, total_questions);

        export_to_csv("lpu_question_bank_export.csv", dataset, total_questions);
        return 0;
    }

    if (argc >= 3 && strcmp(argv[1], "--search") == 0) {
        search_questions(argv[2]);
        return 0;
    }

    if (argc >= 3 && strcmp(argv[1], "--export") == 0) {
        qsort(dataset, total_questions, sizeof(QuestionRecord), compare_marks_desc);
        export_to_csv(argv[2], dataset, total_questions);
        return 0;
    }

    qsort(dataset, total_questions, sizeof(QuestionRecord), compare_marks_desc);
    print_question_records(dataset, total_questions);
    return 0;
}
