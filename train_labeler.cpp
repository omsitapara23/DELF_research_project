#include <bits/stdc++.h>
#include <fstream>
using namespace std;

typedef long long ll;

ifstream train_names("train.txt");
ifstream train_label("train_labels.txt");
// ifstream train4("/../../../../../../media/sdi/dinesh/Landmark/trainFeatures/train4.csv");
// ifstream train5("/../../../../../../media/sdi/dinesh/Landmark/trainFeatures/train5.csv");
// ifstream train0("/../../../../../../media/sdh/landmark/train0.csv");
// ifstream train1("/../../../../../../media/sdb/landmark/train1.csv");
// ifstream train2("/../../../../../../media/sdg/landmark/train2.csv");
// ifstream train3("/../../../../../../media/sdj/landmark/train3.csv");

// ifstream c_train0,c_train1,c_train2,c_train3,c_train4,c_train5;


ofstream outfile;

fstream& Go2Line(fstream& file, unsigned int num)
{
    file.seekg(ios::beg);
    for(unsigned int i=0; i < num - 1; ++i)
        file.ignore(numeric_limits<streamsize>::max(),'\n');

    return file;
}

string seekLine(ifstream& file, int num)
{
    int count = 1;
    string line;
    //cout << "num = " << num << endl;
    while(getline(file,line))
    {
        cout << "count " << count << endl;
        if(count == num)
            return(line);
        count++;

    }
}


int main()
{
    // ios_base::sync_with_stdio(false);
    // cin.tie(NULL);

    // ifstream train0, train1, train2, train3, train4, train5;
    

    //outfile.open("out_labelled_images.txt", ios::app);
    string s;
    int row_no = 1;
    int index;
    vector<int> train_labels;
    int label_in;
    int index_label;
    int read_row;
    int file_no;
    string read_line;
    string out_dir = "/../../../../../../media/sdg/landmark/Class0-8000/class";
    string ext = ".csv";
    vector<int> result[14951];
    while(!train_label.eof())
    {
        train_label >> label_in;
        train_labels.push_back(label_in);
    }
    while(!train_names.eof())
    {
        train_names >> s;
        s = s.substr(0, s.length()- 4);
        index = stoi(s);
        index_label  = train_labels[index];
        result[index_label].push_back(row_no);
        row_no++;
        //cout << index << "\n";
    }
    cout << "done"<<endl;
    
    for(int i = 75; i <= 75; i++)
    {
        cout << "found  =  "<< result[i].size() << endl;
        int temp_readRow0 = 0;
        int temp_readRow1 = 0;
        int temp_readRow2 = 0;
        int temp_readRow3 = 0;
        int temp_readRow4 = 0;
        int temp_readRow5 = 0;
        string temp = out_dir + to_string(i);
        outfile.open( temp + ext, ios::app);
        cout << "opening the file " << endl;
        ifstream train0("/../../../../../../media/sdh/landmark/train0.csv");
        ifstream train1("/../../../../../../media/sdb/landmark/train1.csv");
        ifstream train2("/../../../../../../media/sdg/landmark/train2.csv");
        ifstream train3("/../../../../../../media/sdj/landmark/train3.csv");
        ifstream train4("/../../../../../../media/sdi/dinesh/Landmark/trainFeatures/train4.csv");
        ifstream train5("/../../../../../../media/sdi/dinesh/Landmark/trainFeatures/train5.csv");
        for(int j = 1; j < result[i].size(); j++)
        {
           cout << " j =  " << j << endl;
           read_row = result[i][j];
           file_no = read_row/200000;
           
           if(file_no == 0)
           {
                          
                read_line = seekLine(train0, read_row - temp_readRow0);
                temp_readRow0 = read_row;
                outfile << read_line << "\n";
           }
           else if(file_no == 1)
           {   
                    train0.close();
                    //c_train1 = train1;
                    read_line = seekLine(train1, read_row - 200000 - temp_readRow1);
                    temp_readRow1 = read_row;
                    outfile << read_line << "\n";
            }
            else if(file_no == 2)
           {
                     train1.close();
                    //c_train2 = train2;
                    read_line = seekLine(train2, read_row - 400000 - temp_readRow2);
                    temp_readRow2 = read_row;
                    outfile << read_line << "\n";
            }
            else if(file_no == 3)
           {
                     train2.close();            
                    //c_train3 = train3;
                    read_line = seekLine(train3, read_row - 600000 - temp_readRow3);
                    temp_readRow3 = read_row;
                    outfile << read_line << "\n";
            }
            else if(file_no == 4)
            {
                     train3.close();
                    //c_train4 = train4;
                    read_line = seekLine(train4, read_row - 800000 - temp_readRow4);
                    temp_readRow4 = read_row;
                    outfile << read_line << "\n";
            }
            else
            {
                     train4.close();
                   // c_train5 = train5;
                    read_line = seekLine(train5, read_row - 1000000 - temp_readRow5);
                    temp_readRow5 = read_row;
                    outfile << read_line << "\n";

           } 
        }
        //outfile << "\n";
    }


    return 0;

}