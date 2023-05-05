package com.example.myapplication;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.util.Random;

public class MainActivity extends AppCompatActivity {
    private TextView numberTextView;
    private Button secondActivityButton;
    private NumberUpdaterTask numberUpdaterTask;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        numberTextView = findViewById(R.id.numberTextView);
        secondActivityButton = findViewById(R.id.secondActivityButton);
        updateNumber();

        secondActivityButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, SecondActivity.class);
                startActivity(intent);
            }
        });

        numberUpdaterTask = new NumberUpdaterTask(numberTextView);
        numberUpdaterTask.execute();
    }

    private void updateNumber() {
        Random random = new Random();
        int number = random.nextInt(100) + 1;
        numberTextView.setText(String.valueOf(number));
    }
}
