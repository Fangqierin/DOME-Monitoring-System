package com.example.myapplication;

import android.os.AsyncTask;
import android.widget.TextView;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Random;

public class NumberUpdaterTask extends AsyncTask<Void, Integer, Void> {
    private static final String SERVER_URL = "http://192.168.86.47:3000/test";
    private static final int UPDATE_INTERVAL_MS = 2000;

    private TextView numberTextView;
    private boolean running;

    public NumberUpdaterTask(TextView numberTextView) {
        this.numberTextView = numberTextView;
    }

    @Override
    protected Void doInBackground(Void... voids) {
        running = true;
        while (running) {
            try {
                String number = getNumberFromServer();
                publishProgress(Integer.parseInt(number));
                Thread.sleep(UPDATE_INTERVAL_MS);
            } catch (InterruptedException | IOException e) {
                e.printStackTrace();
            }
        }
        return null;
    }

    @Override
    protected void onProgressUpdate(Integer... values) {
        super.onProgressUpdate(values);
        numberTextView.setText(String.valueOf(values[0]));
    }

    @Override
    protected void onCancelled() {
        super.onCancelled();
        running = false;
    }

    private String getNumberFromServer() throws IOException {
        URL url = new URL(SERVER_URL);
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("GET");
        BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
        String inputLine;
        StringBuilder content = new StringBuilder();
        while ((inputLine = in.readLine()) != null) {
            content.append(inputLine);
        }
        in.close();
        con.disconnect();
        return content.toString();
    }
}