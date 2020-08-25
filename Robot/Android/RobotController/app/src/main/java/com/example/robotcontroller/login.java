package com.example.robotcontroller;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.os.Environment;
import android.os.StrictMode;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;

import java.nio.ByteBuffer;
import java.util.stream.Stream;

public class login extends AppCompatActivity {
	Context context = this;
	
	public static final Socket socket_main = new Socket();
	public static final HashMap<String, Socket> sockets = new HashMap<>();
	
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_login);
		
		StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
		StrictMode.setThreadPolicy(policy);
		
		final Button button_SignIn = (Button)findViewById(R.id.button_SignIn);
		final EditText editText_DeviceIP = (EditText)findViewById(R.id.editText_DeviceIP);
		final EditText editText_Email = (EditText)findViewById(R.id.editText_Email);
		final EditText editText_Password = (EditText)findViewById(R.id.editText_Password);
		
		final InetSocketAddress socketAddress = new InetSocketAddress("127.0.0.1", Integer.parseInt("8001"));
		sockets.put("main", socket_main);
		try{
			//socket_main.connect(socketAddress);
		} catch (Exception e){
			Log.d("ERR", "Socket connect failed.");
			//Log.d("ERR",  e.getMessage());
		}
		
		/*
		String extStore = System.getenv("EXTERNAL_STORAGE");
		File folder = new File(extStore);
		String[] listOfFiles = folder.list();
		
		for (int i = 0; i < listOfFiles.length; i++) {
			System.out.println("File " + listOfFiles[i]);
		}
		*/
		
		button_SignIn.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				Socket socket_main = sockets.get("main");
				button_SignIn.setEnabled(false);
				if (socket_main.isConnected() == false){
					try {
						//socket_main.setSoTimeout(1000);
						final InetSocketAddress socketAddress = new InetSocketAddress(editText_DeviceIP.getText().toString(), Integer.parseInt("8080"));
						Log.d("", "Connecting to: " + editText_DeviceIP.getText().toString());
						socket_main.connect(socketAddress, 1000);
					} catch (IOException e) {
						e.printStackTrace();
						Toast.makeText(context, "Failed to connect to device IP.", Toast.LENGTH_SHORT).show();
						Socket socket_new_main = new Socket();
						sockets.put("main", socket_new_main);
					}
				}
				
				if (socket_main.isConnected()){
					try{
						InputStream socketInputStream = socket_main.getInputStream();
						OutputStream socketOutputStream = socket_main.getOutputStream();
						
						ArrayList<Byte> bytes = new ArrayList<Byte>();
						bytes.add((byte)(13 & 0xFF));
						for (byte b : ByteBuffer.allocate(4).putInt(editText_Email.getText().toString().length()).array()){
							bytes.add(b);
						}
						for (byte b : editText_Email.getText().toString().getBytes()) {
							bytes.add(b);
						}
						for (byte b : ByteBuffer.allocate(4).putInt(editText_Password.getText().toString().length()).array()){
							bytes.add(b);
						}
						for (byte b : editText_Password.getText().toString().getBytes()){
							bytes.add(b);
						}
						
						//bytes.add((byte)(0 & 0xFF));
						//bytes.add((byte)(1 & 0xFF));
						//bytes.add((byte)(255 & 0xFF));
						//bytes.set(0, (byte)((bytes.size()-1) & 0xFF));
						
						byte[] bytes1 = new byte[bytes.size()];
						for(int i=0; i<bytes.size();i++){
							bytes1[i] = bytes.get(i);
						}
						
						Log.d("Send:", bytes.toString());
						
						socketOutputStream.write(bytes1);
						
						byte[] socketInputData = new byte[1];
						int socketInputDataCount = 0;
						
						socketInputDataCount = 0;
						while(socketInputDataCount < 1)
							socketInputDataCount += socketInputStream.read(socketInputData, socketInputDataCount, socketInputData.length - socketInputDataCount);
						
						Log.d("RECV", Integer.toString(socketInputData[0]));
						
						if(socketInputData[0] == 14){
							final Intent intent = new Intent(context, Bootloader.class);
							//intent.putExtra("sockets", sockets);
							Bootloader.sockets = sockets;
							
							startActivity(intent);
							finish();
						} else if (socketInputData[0] == 15){
							Toast.makeText(context, "Login failed.", Toast.LENGTH_SHORT).show();
						}
						
						button_SignIn.setEnabled(true);
						
					} catch (Exception e){
						Log.d("ERR",  e.getMessage());
					}
				}
				button_SignIn.setEnabled(true);
				//final Intent intent = new Intent(context, MainActivity.class);
				//startActivity(intent);
				//finish();
			}
		});
		
	}
}
