# -*- coding: utf-8 -*-
"""
@author: Diogo
"""
import serial
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import subprocess
ser = serial.Serial( 'com7', 9600 )
dist = []
time = []
firstLine = True
temperature = []

N_medicoes = 12
medidos = 0
var = 0
N_aluno1 = 1190528
N_aluno2 = 1191039
Nome1 = "Diogo Rafael Costa Moreira"
Nome2 = "Rui Miguel da Silva Teixeira"
Grupo = "1"
Turma = "DB"
t_ms = []
d_mm = []
# Scan de medições
for medidos in range(N_medicoes):
    print("\nInsira a distancia",medidos+1,"em milimetros: ")
    var = input()
    ser.write(bytes(var, 'utf-8'))
    ser.write(bytes('\n', 'utf-8'))
    while (var!=0):
        if ( ser.inWaiting() > 0 ):
                data = ser.readline()[:-2]  
                t_ms, d_mm = data.split()
                time.append( float(t_ms) )
                dist.append( float(d_mm) )
                medidos +=1
                var = 0
data = np.c_[time, dist]
outputFilename = 'Calibration.dat'
np.savetxt( outputFilename, data, fmt='%0.2f', delimiter=" ")

# Remove ultima linha
fd=open("Calibration.dat","r")
d=fd.read()
fd.close()
m=d.split("\n")
s="\n".join(m[:-1])
fd=open("Calibration.dat","w+")
for i in range(len(s)):
    fd.write(s[i])
fd.close()
var = 0
# Scan de temperatura
ser.write(bytes('T', 'utf-8'))
ser.write(bytes('\n', 'utf-8'))
while (var==0):
        if ( ser.inWaiting() > 0 ):
                temperatura = ser.readline()[:-2]
                let, temp = temperatura.split()
                temperature.append( float(temp) )
                var = 1

ser.close();   
# Processamento dos dados
inputFilename = 'Calibration.dat'
temp =  temperature[0]
temp_kelvin = 273.15 + temp
absoluta_temp = 0.05
relativa_temp = 100*absoluta_temp/temp_kelvin
print(temp)

speed_ref = 20.05 *  np.sqrt(temp_kelvin)
absoluta_speedRef = absoluta_temp
relativa_speedRef = 100*(absoluta_speedRef / speed_ref)


data = np.loadtxt( inputFilename, dtype=float, delimiter=" ")
time_ms = data[:,1]
dist_mm = data[:,0]
res=stats.linregress(time_ms,dist_mm)
 

speed_exp = res.slope*2;
absoluta_exp = res.stderr
relativa_exp = 100 * (absoluta_exp / speed_exp)

deviation = 100*(abs(speed_ref-speed_exp)/speed_ref)

fig = plt.figure()
fig.add_subplot(1,1,1)
plt.xlabel("Time, t(ms)", fontsize=14)
plt.ylabel("Distance, d(mm)", fontsize=14)
plt.axis([0,7,0,1300])
plt.plot(time_ms, dist_mm, 'o', label='Experimental')
plt.plot(time_ms,res.slope*time_ms+ res.intercept, 'r', label='linear fit')
plt.legend()
plt.grid(True)
plt.show()

outputFile = "Calibration.png"
plt.savefig(outputFile)
# Latex e PDF

string = """%%####################################################
% Apendice_Sonar.tex
% Diogo Moreira, Rui Teixeira
% Janeiro 2022
%####################################################
\\documentclass[11pt,a4paper,oneside]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[portuges]{babel}
\\usepackage[portuguese]{babel}
%\\usepackage[english]{babel}
\\usepackage[latin1]{inputenc}
% Para adicionar a língua (PT)
\\usepackage[portuges]{babel}
% suporte para utf8
\\usepackage[utf8]{inputenc}
\\usepackage{aeguill}
\\usepackage{setspace}
%\\usepackage[top=3cm,left=3cm,right=3cm,foot=1.5cm,bottom=3cm]{geometry}
\\usepackage[top=2.5cm,left=2.5cm,right=2.5cm,bottom=2.5cm]{geometry}

\\usepackage{listings}								% to list C++ programs
\\usepackage[small,bf]{caption}
\\usepackage{color}
\\usepackage{graphicx}
\\usepackage{subfigure}
\\usepackage{tabularx}
\\usepackage{multirow}
\\usepackage{multicol}
\\usepackage{amsmath}
\\usepackage{makeidx}
\\usepackage{hyperref}
\\hypersetup{
    %bookmarks=true,    	     	 % show bookmarks bar?
    unicode=false,      	   		 % non-Latin characters in Acrobats bookmarks
    pdftoolbar=true,    		     % show Acrobats toolbar?
    pdfmenubar=true,        	  	 % show Acrobats menu?
    pdffitwindow=true,     		  	 % window fit to page when opened
    pdfstartview={FitH},    	  	 % fits the width of the page to the window
    pdftitle={VIBON Report},		 % title
    pdfauthor={author},      	% author
    pdfsubject={Template Report},    % subject of the document
    pdfcreator={},   				 	% creator of the document
    pdfproducer={}, 				 	% producer of the document
    pdfkeywords={},                  % list of keywords
    pdfnewwindow=true,  		     % links in new window
    colorlinks=true,    		     % false: boxed links; true: colored links
    linkcolor=blue,      		     % color of internal links
    citecolor=green,    		     % color of links to bibliography
    filecolor=magenta,  		     % color of file links
    urlcolor=red        			 % color of external links
}
\\usepackage{pdfpages}
\\usepackage{rotating}
\\usepackage{microtype}
\\usepackage{float}


%####################################################
\\begin{document}
%####################################################

%================================================================================
\\section*{Apêndice} % PT
%\\section*{Appendix} % EN
%\\label{sec:appendix}
\\addcontentsline{toc}{chapter}{Apêndice} % PT
%\\addcontentsline{toc}{chapter}{Appendix} % EN
%================================================================================
\\begin{center} \\Large VIBON 2021/2022 \\end{center}
\\begin{center} \\Large \\textcolor[rgb]{1,0,0}{\\textbf{Trabalho SONAR}} \\end{center}
%================================================================================


%-----------------------------
%Tabela~\\ref{tab:GRUPO}
%Tabela~\\ref{tab:ALUNOS}
%-----------------------------
\\begin{table}[!htb]
	\\centering
		\\begin{tabular}{ |m{2cm} m{1cm} | m{2cm} m{1cm} |m{2.6cm} m{2.6cm} |}
			\\hline \\noalign{\\smallskip}
			\\textbf{Turma}: & 3"""+Turma+""" & \\textbf{Grupo}: & """+Grupo+""" & \\textbf{Data}: &  ?? / 01 / 2022 \\\\ \\noalign{\\smallskip}
			\\hline
		\\end{tabular}
		\\begin{tabular}{ |m{2cm} m{1cm} | m{6cm} m{1cm} m{0.6cm} m{0.6cm} |}
			\\hline \\noalign{\\smallskip}
			\\textbf{Número} & & \\textbf{Nome} (assinatura) & & & \\\\ \\noalign{\\smallskip} 
			\\hline \\noalign{\\smallskip}
			"""+str(N_aluno1)+"""& &"""+Nome1+""" & & & \\\\ \\noalign{\\smallskip} 			\\hline \\noalign{\\smallskip}
			"""+str(N_aluno2)+""" & &"""+Nome2+""" & & & \\\\ \\noalign{\\smallskip} 			\\hline \\noalign{\\smallskip}
			? & & & & & \\\\ \\noalign{\\smallskip} 			\\hline \\noalign{\\smallskip}
			? & & & & & \\\\ \\noalign{\\smallskip} 
			\\hline
		\\end{tabular}
\\end{table}
%%-----------------------------

\\bigskip
%====================================================
\\begin{center} \\Large \\textbf{Registo de Dados} \\end{center}
%====================================================
%-----------------------------
%Tabela~\\ref{tab:SONAR}
%Tabela~\\ref{tab:HOOKE}
%-----------------------------
\\begin{table}[!htb]
	\\begin{minipage}{.5\\linewidth}	
		\\centering
		\\caption[Calibração SONAR]{Calibração SONAR.}
		\\label{tab:SONAR}		
		%\\begin{tabular}{@{\\extracolsep{0 mm}}|c|c|}
		\\begin{tabular}{| m{2.5cm} | m{2.5cm} |}
			\\hline % \\noalign{\\smallskip}
			\\textbf{Distância} & \\textbf{Tempo Eco} \\\\ 
			$d$ (mm)  & ${t_{eco}}$ (ms) \\\\ \\hline \\noalign{\\smallskip}
			"""+str(dist_mm[0])+"""&"""+str(time_ms[0])+""" \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			"""+str(dist_mm[1])+"""&"""+str(time_ms[1])+""" \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			"""+str(dist_mm[2])+"""& """+str(time_ms[2])+"""\\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			"""+str(dist_mm[3])+"""&"""+str(time_ms[3])+""" \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			"""+str(dist_mm[4])+"""&"""+str(time_ms[4])+""" \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			"""+str(dist_mm[5])+"""&"""+str(time_ms[5])+""" \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			"""+str(dist_mm[6])+"""&"""+str(time_ms[6])+""" \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			"""+str(dist_mm[7])+"""& """+str(time_ms[7])+"""\\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			"""+str(dist_mm[8])+"""&"""+str(time_ms[8])+""" \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			"""+str(dist_mm[9])+"""& """+str(time_ms[9])+"""\\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}			
			"""+str(dist_mm[10])+"""&"""+str(time_ms[10])+""" \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			"""+str(dist_mm[11])+"""&"""+str(time_ms[11])+""" \\\\ \\noalign{\\smallskip} \\hline		
		\\end{tabular}
	\\end{minipage}%	
	\\begin{minipage}{.5\\linewidth}
		\\centering
		\\caption[Lei de Hooke]{Lei de HOOKE.}
		\\label{tab:HOOKE}
		%\\begin{tabular}{@{\\extracolsep{0 mm}}|c|c|}	
		\\begin{tabular}{| m{2.5cm} | m{2.5cm} |}
			\\hline 
			\\textbf{Massa} & \\textbf{Distância}  \\\\ 
			$m$ (g)        & $d$ (mm)  	         \\\\ \\hline \\noalign{\\smallskip}
			& \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			& \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			& \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			& \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			& \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			& \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			& \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			& \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			& \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			& \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}			
			& \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			& \\\\ \\noalign{\\smallskip} \\hline		
		\\end{tabular}
	\\end{minipage} 
\\end{table}
%-----------------------------


\\vfill
\\pagebreak
%====================================================
\\begin{center} 
\\Large \\textbf{Registo de Resultados} 
\\end{center}
%====================================================
%-----------------------------
%Tabela~\\ref{tab:Resultados1}
\\begin{table}[!htb]
\\small
	\\centering
		\\caption[]{Resultados -- Calibração do SONAR.}
		\\label{tab:Resultados1}	
		\\begin{tabular}{| m{5cm} | m{2.2cm} | m{2.2cm} | m{2.2cm} | m{2.2cm} | }
		\\hline \\noalign{\\smallskip}
			\\textbf{Grandeza} & \\textbf{Símbolo} & \\textbf{Valor} & \\textbf{Incerteza} & \\textbf{Incerteza} \\\\
												& (unidade)        &                & \\textbf{padrão}    & \\textbf{relativa} ($\\%$) \\\\
			\\hline \\noalign{\\smallskip}
			Temperatura ambiente        & $\\Theta _1$ (K)        &"""+str(temp_kelvin)+""" &"""+str(absoluta_temp)+"""    & """+str("{:.3f}".format(relativa_temp)) +"""   \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			Velocidade do som (ref.)    & $v_{ref}$ (m s$^{-1}$) &"""+str("{:.3f}".format(speed_ref)) +"""  &"""+str("{:.3f}".format(absoluta_speedRef)) +"""     & """+str("{:.3f}".format(relativa_speedRef)) +"""    \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
			Velocidade do som (exp.)    & $v_{som}$ (m s$^{-1}$) & """+str("{:.3f}".format(speed_exp)) +""" & """+str("{:.3f}".format(absoluta_exp)) +"""    &"""+str("{:.3f}".format(relativa_exp)) +"""     \\\\ \\noalign{\\smallskip} 	\\hline \\noalign{\\smallskip}
			Desvio relativo (exactidão) & $\\Delta v$ ($\\%$)        &"""+str("{:.3f}".format(deviation)) +"""  & -- & -- \\\\ \\noalign{\\smallskip} \\hline
		\\end{tabular}
\\end{table}
%-----------------------------
%\\vfill
%-----------------------------
%Tabela~\\ref{tab:Resultados2}
\\begin{table}[!htb]
\\small
	\\centering
	\\caption[]{Resultados -- Lei de Hooke.}
	\\label{tab:Resultados2}		
	\\begin{tabular}{| m{5cm} | m{2.2cm} | m{2.2cm} | m{2.2cm} | m{2.2cm} | }
		\\hline \\noalign{\\smallskip}
		\\textbf{Grandeza} & \\textbf{Símbolo} & \\textbf{Valor} & \\textbf{Incerteza} & \\textbf{Incerteza} \\\\
											& (unidade)        &                & \\textbf{padrão}    & \\textbf{relativa} ($\\%$) \\\\
		\\hline \\noalign{\\smallskip}
		
		%Temperatura ambiente        & $\\Theta _2$ (K) & & & \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
		%Comprimento natural da mola   & $l_0$        & & & \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
		%Massa da mola                 & $l_0$        & & & \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}				
    Massa do suporte com placa    & $m_0$ (g)   & & & \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
		Distância inicial             & $d_0$ (mm)  & & & \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
		Constante elástica da mola    & $k$   (N/m) & & & \\\\ \\noalign{\\smallskip} \\hline
		
	\\end{tabular}
\\end{table}
%-----------------------------
%\\vfill
%-----------------------------
%Tabela~\\ref{tab:Resultados3}
\\begin{table}[!htb]
	\\small
	\\centering
	\\caption[]{Resultados -- Oscilador Amortecido.}
	\\label{tab:Resultados3}		
	\\begin{tabular}{| m{5cm} | m{2.2cm} | m{2.2cm} | m{2.2cm} | m{2.2cm} | }
		\\hline \\noalign{\\smallskip}
		\\textbf{Grandeza} & \\textbf{Símbolo} & \\textbf{Valor} & \\textbf{Incerteza} & \\textbf{Incerteza} \\\\
											& (unidade)        &                & \\textbf{padrão}    & \\textbf{relativa} ($\\%$) \\\\
		\\hline \\noalign{\\smallskip}
		
		%Temperatura ambiente         & $\\Theta _3$ (K) & & & \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
		Massa do corpo suspenso       & $m$ (g)                   & & & \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
		Massa total do oscilador      & $M$ (g)                   & & & \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
		Distância inicial             & $d_0$ (mm)                & & & \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
		Período de oscilação (zeros)  & $T_{zeros}$ (s)           & & & \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
		Período de oscilação (picos)  & $T_{peaks}$ (s)           & & & \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
		Desvio relativo (exactidão)   & $\\Delta T$ ($\\%$)         & & -- & -- \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
		Coef. de Amortecimento        & $\\gamma$ (s$^{-1}$)       & & & \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
		Frequência própria            & $\\omega_0 $ (rad s$^{-1}$) & & & \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
		Frequência de oscilação       & $\\omega$   (rad s$^{-1}$) & & & \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
		Período de oscilação (calc)   & $T_{calc}$ (s$^{-1}$)     & & & \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
		Factor de qualidade           & $Q$                       & & & \\\\ \\noalign{\\smallskip} \\hline \\noalign{\\smallskip}
		Decaimento (amplitude)        & $\\tau$     (s$^{-1}$)     & & & \\\\ \\noalign{\\smallskip} \\hline

	\\end{tabular}
\\end{table}
%-----------------------------





%####################################################
\\end{document}
%####################################################



"""

with open("./apendice.tex", "w") as f:
     f.write(string.strip())
     
subprocess.run(['pdflatex', '-interaction=nonstopmode', "apendice.tex"])
# subprocess.check_call(['pdflatex', 'mylatex.tex'])












