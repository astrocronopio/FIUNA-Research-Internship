
/// Program to assign the solar weather info for each event from the Muons events
///
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>

using namespace std;

int main(int argc, char** argv)
{
	ifstream muondata 	("../../../Local-Machine/Datasets/Muons/vertical_total_muons_30-min_bin.txt");
	ifstream rtswdata 	("../../../Local-Machine/Datasets/Solar_Weather/rtsw_utc_plot_data_30-min_bin.txt");
	ofstream outfile 	("../../../Local-Machine/Datasets/muons_rtsw_merged_data_30-min_bin.txt");

	string linemuon;
	string linertsw;

	float binWidth = 1800; 

	if(muondata.is_open() && rtswdata.is_open())	
	{
		int iutc,utc;		
		float phi;
	
		getline(rtswdata,linertsw);
		stringstream srtsw(linertsw);
		
        srtsw >> iutc >> phi;
		
		while (!muondata.eof() && !rtswdata.eof() )
		{
			getline(muondata,linemuon);			
			stringstream smuon(linemuon);			
			
			smuon >> utc ;
			

			while (!rtswdata.eof() ){			
				if(utc <= iutc && utc > iutc-binWidth )
				{	
					outfile << linemuon <<"\t" << phi  << "\n";
					
					outfile.flush();
					break;
				}
				else{
					getline(rtswdata,linertsw);
					stringstream srtsw(linertsw);
					srtsw >> iutc >> phi;
					continue;
				}
			}			
		}
		muondata.close();
		rtswdata.close();
		outfile.close();
	}
	else cout << "Unable to open file"; 

	std::cout<<"done!\n";
	return 0;
}
