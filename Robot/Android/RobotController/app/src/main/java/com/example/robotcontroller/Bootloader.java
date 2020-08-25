package com.example.robotcontroller;

import androidx.appcompat.app.AppCompatActivity;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.WindowManager;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckedTextView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class Bootloader extends AppCompatActivity {
	
	public static HashMap<String, Socket> sockets;
	
	
	Context context = this;
	
	private byte[] recieve(Socket socket, int length){
		try{
			InputStream socketInputStream = socket.getInputStream();
			
			byte[] socketInputData = new byte[length];
			int socketInputDataCount = 0;
			
			socketInputDataCount = 0;
			while (socketInputDataCount < length) {
				socketInputDataCount += socketInputStream.read(socketInputData, socketInputDataCount, socketInputData.length - socketInputDataCount);
			}
			
			return socketInputData;
		} catch (Exception e) {
			Log.d("ERR", e.getMessage());
			return null;
		}
	}
	
	public static void send(Socket socket, byte[] bytes){
		try{
			OutputStream socketOutputStream = socket.getOutputStream();
			socketOutputStream.write(bytes);
		} catch (Exception e){
			Log.d("ERR", e.getMessage());
		}
	}
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_bootloader);
		
		final Socket socket_main = (Socket)sockets.get("main");
		
		final LinearLayout rootLayout = (LinearLayout)findViewById(R.id.rootLayout);
		final Button Button_UploadFile = (Button)findViewById(R.id.Button_UploadFile);
		final Button Button_CancelExecution = (Button)findViewById(R.id.Button_CancelExecution);
		
		final LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		
		if (recieve(socket_main, 1)[0] == 12){
			int files_count = recieve(socket_main, 1)[0];
			for (int i =0; i<files_count; i++){
				final int file_name_size = recieve(socket_main, 1)[0];
				final String file_name = new String(recieve(socket_main, file_name_size));
				
				Button button = new Button(context);
				button.setText(file_name);
				
				LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
						LinearLayout.LayoutParams.WRAP_CONTENT,
						LinearLayout.LayoutParams.WRAP_CONTENT
				);
				params.setMargins(10,0,10,10);
				button.setLayoutParams(params);
				
				button.setOnClickListener(new View.OnClickListener() {
					@Override
					public void onClick(View v) {
						ArrayList<Byte> bytes = new ArrayList<Byte>();
						bytes.add((byte)(11 & 0xFF));
						for (byte b : ByteBuffer.allocate(4).putInt(file_name_size).array()){
							bytes.add(b);
						}
						for (byte b : file_name.getBytes()) {
							bytes.add(b);
						}
						
						byte[] bytes1 = new byte[bytes.size()];
						for(int i=0; i<bytes.size();i++){
							bytes1[i] = bytes.get(i);
						}
						
						Log.d("Send:", bytes.toString());
						
						send(socket_main, bytes1);
						
						//rootLayout.setEnabled(false);
						Toast.makeText(context, "Loading file.", Toast.LENGTH_SHORT).show();
						//getWindow().setFlags(WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE, WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE);
						
						for (int i = 0; i < rootLayout.getChildCount(); i++) {
							View child = rootLayout.getChildAt(i);
							child.setEnabled(false);
						}
						
						Button_UploadFile.setEnabled(false);
						Button_CancelExecution.setEnabled(true);
						
						Thread socket_thread = new Thread(new Runnable() {
							@Override
							public void run() {
								while (true){
									int status = recieve(socket_main, 1)[0];
									if (status == 16){
										runOnUiThread(new Runnable() {
											@Override
											public void run() {
												//rootLayout.setEnabled(true);
												//getWindow().clearFlags(WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE);
												for (int i = 0; i < rootLayout.getChildCount(); i++) {
													View child = rootLayout.getChildAt(i);
													child.setEnabled(true);
												}
												
												Button_UploadFile.setEnabled(true);
												Button_CancelExecution.setEnabled(false);
												Toast.makeText(context, "Execution ended.", Toast.LENGTH_SHORT).show();
											}
										});
										
									} else if (status == 17){
										final Intent intent = new Intent(context, MainActivity.class);
										MainActivity.sockets = sockets;
										startActivity(intent);
										runOnUiThread(new Runnable() {
											@Override
											public void run() {
												//finish();
											}
										});
										//return;
									}
								}
								
							}
						});
						
						socket_thread.start();
						
					}
				});
				
				rootLayout.addView(button);
			}
			
			//rootLayout.setEnabled(false);
		}
		
		Button_UploadFile.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				final AlertDialog.Builder uploadFileDialog = new AlertDialog.Builder(context);
				uploadFileDialog.setTitle("File upload");
				uploadFileDialog.setMessage("Select the files you wish to upload the ESP32.");
				
				ListView uploadFilesListView = new ListView(context);
				
				uploadFileDialog.setView(uploadFilesListView);
				
				final List<String> uploadFilesList = new ArrayList<String>();
				
				final ArrayAdapter<String> adapterFiles = new ArrayAdapter<String>(context,
						android.R.layout.simple_list_item_multiple_choice, android.R.id.text1, uploadFilesList);
				
				uploadFilesListView.setAdapter(adapterFiles);
				
				//This is bugged
				//https://stackoverflow.com/questions/11382539/trouble-with-android-listview-selection-changes-when-switching-choicemode
				uploadFilesListView.setChoiceMode(ListView.CHOICE_MODE_MULTIPLE);
				
				//When an item in the list view is clicked, we want to toggle its checkbox
				uploadFilesListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
					@Override
					public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
						CheckedTextView checkedTextView = ((CheckedTextView) view);
						checkedTextView.setChecked(!checkedTextView.isChecked());
					}
				});
				
				uploadFileDialog.setPositiveButton("Upload", new DialogInterface.OnClickListener() {
					@Override
					public void onClick(DialogInterface dialog, int which) {
						
					}
				});
				
				uploadFileDialog.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
					@Override
					public void onClick(DialogInterface dialog, int which) {
					
					}
				});
				
				uploadFileDialog.show();
			}
		});
		
		Button_CancelExecution.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				final Socket socket_main = sockets.get("main");
				if (socket_main.isConnected()){
					byte[] bytes = new byte[1];
					bytes[0] = 18;
					Bootloader.send(socket_main, bytes);
				}
			}
		});
		
	}
}
