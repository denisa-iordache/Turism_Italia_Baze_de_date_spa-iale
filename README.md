# Turism_Italia_Baze_de_date_spatiale
## Tehnologii folosite
• Proiectul a fost realizat in ArcGIS Pro, integrând pentru prelucrarea datelor un script Python. <br/>
• Am folosit o baza de date de tip geodatabase, scopul proiectului fiind lucrul cu baze de date spațiale.<br/>
• Datele au fost preluate de pe mapcruzin.com și hub.arcgis.com.
## Descrierea aplicației
• Scriptul integrat in ArcGis are o interfață ce permite utilizatorului să pună până la 3 condiții pentru a obține rezultatul dorit. Câmpurile obligatorii sunt marcate cu „*”. Astfel, trebuie specificate tabelele din baza de date și prima contiție ce reprezintă comuna din care doresc să afișez punctele de interes.<br/>
• A doua condiție se referă la tipul de punct de interes ce doresc să fie afișat (fuel,museum,school,etc.)<br/>
• A treia condiție ia in considerare situația in care un turist se află pe un drum anume și dorește să vadă ce puncte de interes se găsesc pe o rază de 2 km de acel drum.<br/>
• Fiecare punct de interes are o simbologie diferită pe hartă, asemănător Google Maps. Și acest lucru este realizat tot în scriptul Python.
• Rezultatele rulării scriptului se salvează în baza de date.
## Capturi de ecran din aplicație
• Harta Italiei cu toate comunele, drumurile și punctele de interes (înainte de aplicarea simbologiei) <br/><br/>
![image](https://user-images.githubusercontent.com/74931542/220342763-b5ab4c39-cf65-4944-9b64-1725dfa62d35.png)
<br/><br/>
• Afișarea tuturor punctelor de interes din comuna Trento <br/><br/>
![image](https://user-images.githubusercontent.com/74931542/220346571-d6b9d346-28b3-4104-be6e-c35814baa943.png)
![image](https://user-images.githubusercontent.com/74931542/220346647-9c50c4dc-0bb2-428d-97de-0803a8fe5828.png)
<br/><br/>
• Afișarea benzinăriilor din comuna Trento <br/><br/>
![image](https://user-images.githubusercontent.com/74931542/220346194-fdbb27de-cb1a-4499-b02e-ff79adf0b31a.png)
<br/><br/>
• Afișarea benzinăriilor din comuna Trento situate la maxim 2 km de drumul lung'Adige Giacomo Leopardi <br/><br/>
![image](https://user-images.githubusercontent.com/74931542/220347531-d3442a0d-d23e-493f-8075-27232544f097.png)
