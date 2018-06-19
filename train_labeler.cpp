#include <bits/stdc++.h>

using namespace std;

typedef long long ll;

ifstream train_names("train.txt");
ifstream train_label("train_labels.txt");
ofstream outfile;

fstream& Go2Line(fstream& file, unsigned int num)
{
    file.seekg(ios::beg);
    for(unsigned int i=0; i < num - 1; ++i)
        file.ignore(numeric_limits<streamsize>::max(),'\n');

    return file;
}


int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); 

    outfile.open("out_labelled_images.txt", ios::app);
    string s;
    int row_no = 1;
    int index;
    vector<int> train_labels;
    int label_in;
    int index_label;
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
        cout << index << "\n";
    }

    for(int i = 0; i < 14951; i++)
    {
        for(int j = 0; j < result[i].size(); j++)
        {
            outfile << result[i][j] << " ";
        }
        outfile << "\n";
    }

    return 0;

}