package com.example.robotcontroller;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.os.Bundle;
import android.os.StrictMode;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.LinearLayout;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.SeekBar;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.ToggleButton;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.lang.reflect.Array;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

public class MainActivity extends AppCompatActivity {
	
	public static HashMap<String, Socket> sockets;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		final Socket socket_main = sockets.get("main");
		
		final SeekBar SeekBar_left = (SeekBar)findViewById(R.id.SeekBar_left);
		SeekBar SeekBar_right = (SeekBar)findViewById(R.id.SeekBar_right);
		
		Button button = (Button)findViewById(R.id.button);
		button.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				SeekBar_left.setProgress(0);
			}
		});
		
		ToggleButton ToggleButton_GPIO24 = (ToggleButton)findViewById(R.id.ToggleButton_GPIO24);
		
		final TextView textView = (TextView)findViewById(R.id.textView);
		
		View.OnFocusChangeListener onFocusChangeListener = new View.OnFocusChangeListener() {
			@Override
			public void onFocusChange(View v, boolean hasFocus) {
				if (!hasFocus) {
					((SeekBar) v).setProgress(0);
				}
			}
		};
		
		View.OnTouchListener onTouchListener = new View.OnTouchListener() {
			@Override
			public boolean onTouch(View v, MotionEvent event) {
				Log.d("EVENT", String.valueOf(event.getAction()));
				if (event.getAction() == MotionEvent.ACTION_UP){
					((SeekBar) v).setProgress(0);
				}
				return false;
			}
		};
		
		
		SeekBar_left.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
			@Override
			public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
				try{
					PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket_main.getOutputStream())), true);
					
					InputStream socketInputStream = socket_main.getInputStream();
					OutputStream socketOutputStream = socket_main.getOutputStream();
					
					byte[] socketInputData = new byte[1024];
					int socketInputDataCount = 0;
					
					
					while(true){
						ArrayList<Byte> bytes = new ArrayList<Byte>();
						bytes.add((byte)(1 & 0xFF));
						bytes.add((byte)(0 & 0xFF));
						bytes.add((byte)(1 & 0xFF));
						bytes.add((byte)(255 & 0xFF));
						bytes.set(0, (byte)((bytes.size()-1) & 0xFF));
						
						byte[] bytes1 = new byte[bytes.size()];
						for(int i=0; i<bytes.size();i++){
							bytes1[i] = bytes.get(i);
						}
						
						bytes1[bytes.size()-1] = (byte)progress;
						
						Log.d("Send:", bytes.toString());
						
						socketOutputStream.write(bytes1);
						
						break;
					}
					
				} catch (Exception e){
				
				}
				
			}
			
			@Override
			public void onStartTrackingTouch(SeekBar seekBar) {
			
			}
			
			@Override
			public void onStopTrackingTouch(SeekBar seekBar) {
			
			}
		});
		//SeekBar_left.setOnFocusChangeListener(onFocusChangeListener);
		//SeekBar_right.setOnFocusChangeListener(onFocusChangeListener);
		
		SeekBar_left.setOnTouchListener(onTouchListener);
		SeekBar_right.setOnTouchListener(onTouchListener);
		
		if (true)
			;//return;
		
		
		StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
		StrictMode.setThreadPolicy(policy);
		
		
		Thread socketThread = new Thread(){
			public void run(){
				try {
					BufferedReader in = new BufferedReader(new InputStreamReader(socket_main.getInputStream(), "UTF-8"));
					PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket_main.getOutputStream())), true);
					
					InputStream socketInputStream = socket_main.getInputStream();
					OutputStream socketOutputStream = socket_main.getOutputStream();
					
					byte[] socketInputData = new byte[1024];
					int socketInputDataCount = 0;
					
					boolean a = false;
					while(a){
						
						socketInputDataCount = 0;
						while(socketInputDataCount < 1){
							socketInputDataCount += socketInputStream.read(socketInputData, socketInputDataCount, socketInputData.length - socketInputDataCount);
						}
						
						final String socketInputDataString = new String(Arrays.copyOfRange(socketInputData, 0, socketInputDataCount), "UTF-8");
						//socketInputDataString += '\n';
						
						Log.d("TEST", "TEST");
						Log.d("MSG",  socketInputDataString);
						
						runOnUiThread(new Runnable() {
							@Override
							public void run() {
								textView.setText(socketInputDataString);
							}
						});
						
						//out.println("Read from server: " + socketInputDataString);
						
						//socketOutputStream.write(("Recieved from server:" + socketInputDataString).getBytes(Charset.forName("UTF-8")));
						byte[] data = new byte[]{2,1,2};
						socketOutputStream.write(data);
				
				/*
				String readFromServer = in.readLine();
				Log.d("MSG",  readFromServer);
				out.println("Read from server: " + readFromServer);
				
				 */
						
						ArrayList<Byte> bytes = new ArrayList<Byte>();
						bytes.add((byte)(1 & 0xFF));
						bytes.add((byte)(0 & 0xFF));
						bytes.add((byte)(1 & 0xFF));
						bytes.add((byte)(255 & 0xFF));
						bytes.set(0, (byte)((bytes.size()-1) & 0xFF));
						
						byte[] bytes1 = new byte[bytes.size()];
						for(int i=0; i<bytes.size();i++){
							bytes1[i] = bytes.get(i);
						}
						
						Log.d("Send:", bytes.toString());
						
						socketOutputStream.write(bytes1);
						
						//break;
					}
					
					
					
					
				} catch (IOException e) {
					Log.d("ERROR", e.getMessage());
					e.printStackTrace();
				}
			}
		};//.run();
		
		//socketThread.start();
		
		ToggleButton_GPIO24.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
			@Override
			public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
				if (!socket_main.isConnected())
					return;
				OutputStream socketOutputStream = null;
				try {
					socketOutputStream = socket_main.getOutputStream();
					
					ArrayList<Byte> bytes = new ArrayList<Byte>();
					bytes.add((byte)(3 & 0xFF));
					bytes.add((byte)(255 & 0xFF));
					bytes.add((byte)(24 & 0xFF));
					int checkValue = isChecked?1:0;
					bytes.add((byte)(checkValue & 0xFF));
					bytes.set(0, (byte)((bytes.size()-1) & 0xFF));
					
					byte[] bytes1 = new byte[bytes.size()];
					for(int i=0; i<bytes.size();i++){
						bytes1[i] = bytes.get(i);
					}
					
					Log.d("Send:", bytes.toString());
					
					socketOutputStream.write(bytes1);
					
				} catch (IOException e) {
					Log.d("ERROR", e.getMessage());
					e.printStackTrace();
				}
			}
		});
		
		int[] GPIO_Pins = new int[]{2, 4, 5, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 32, 33, 34, 35, 36, 39};
		ArrayList<Integer> ArrayList_GPIO_Pins = new ArrayList<>();
		for (int i : GPIO_Pins){
			ArrayList_GPIO_Pins.add(i);
		}
		
		int[] GPIO_InputOnlyPins = new int[]{34,35,36,39};
		ArrayList<Integer> ArrayList_GPIO_InputOnlyPins = new ArrayList<>();
		for (int i : GPIO_InputOnlyPins){
			ArrayList_GPIO_InputOnlyPins.add(i);
		}
		
		LayoutInflater mInflater = (LayoutInflater) this.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		LinearLayout linearLayout = (LinearLayout)findViewById(R.id.LinearLayout_Parent);
		for(final int i : GPIO_Pins){
			
			final View view = mInflater.inflate(R.layout.pincontrollayout, linearLayout, false);
			
			Button Button_Apply = (Button)view.findViewById(R.id.Button_Apply);
			
			TextView textView1 = (TextView)view.findViewById(R.id.TextView_PinName);
			textView1.setText(Integer.toString(i));
			
			final RadioGroup RadioGroup_Mode = (RadioGroup)view.findViewById(R.id.RadioGroup_Mode);
			
			final LinearLayout LinearLayout_PinSettings = (LinearLayout)view.findViewById(R.id.LinearLayout_PinSettings);
			LinearLayout_PinSettings.setVisibility(View.GONE);
			
			final LinearLayout LinearLayout_Input = (LinearLayout)view.findViewById(R.id.LinearLayout_Input);
			final LinearLayout LinearLayout_Output = (LinearLayout)view.findViewById(R.id.LinearLayout_Output);
			final LinearLayout LinearLayout_OutputDigital = (LinearLayout)view.findViewById(R.id.LinearLayout_OutputDigital);
			final LinearLayout LinearLayout_OutputPWM = (LinearLayout)view.findViewById(R.id.LinearLayout_OutputPWM);
			
			final RadioGroup RadioGroup_Input = (RadioGroup)view.findViewById(R.id.RadioGroup_Input);
			final RadioGroup RadioGroup_Output = (RadioGroup)view.findViewById(R.id.RadioGroup_Output);
			final RadioGroup RadioGroup_OutputDigital = (RadioGroup)view.findViewById(R.id.RadioGroup_OutputDigital);
			
			Switch Switch_Pin = view.findViewById(R.id.Switch_Pin);
			Switch_Pin.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
				@Override
				public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
					if (isChecked){
						LinearLayout_PinSettings.setVisibility(View.VISIBLE);
					} else {
						LinearLayout_PinSettings.setVisibility(View.GONE);
					}
				}
			});
			
			RadioGroup_Mode.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
				@Override
				public void onCheckedChanged(RadioGroup group, int checkedId) {
					if (checkedId == R.id.RadioButton_ModeInput){
						LinearLayout_Input.setVisibility(View.VISIBLE);
						LinearLayout_Output.setVisibility(View.GONE);
					} else if (checkedId == R.id.RadioButton_ModeOutput){
						LinearLayout_Input.setVisibility(View.GONE);
						LinearLayout_Output.setVisibility(View.VISIBLE);
					}
				}
			});
			
			RadioGroup_Input.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
				@Override
				public void onCheckedChanged(RadioGroup group, int checkedId) {
					if (checkedId == R.id.RadioButton_InputDigital){
					
					} else if (checkedId == R.id.RadioButton_InputAnalog){
					
					}
				}
			});
			
			RadioGroup_Output.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
				@Override
				public void onCheckedChanged(RadioGroup group, int checkedId) {
					if (checkedId == R.id.RadioButton_OutputDigital){
						LinearLayout_OutputDigital.setVisibility(View.VISIBLE);
						LinearLayout_OutputPWM.setVisibility(View.GONE);
					} else if (checkedId == R.id.RadioButton_OutputPWM){
						LinearLayout_OutputDigital.setVisibility(View.GONE);
						LinearLayout_OutputPWM.setVisibility(View.VISIBLE);
					}
				}
			});
			
			
			final SeekBar SeekBar_DutyCycle = (SeekBar)view.findViewById(R.id.SeekBar_DutyCycle);
			final TextView TextView_DutyCycle = (TextView)view.findViewById(R.id.TextView_DutyCycle);
			
			final SeekBar SeekBar_Frequency = (SeekBar)view.findViewById(R.id.SeekBar_Frequency);
			final TextView TextView_Frequency = (TextView)view.findViewById(R.id.TextView_Frequency);
			
			TextView_DutyCycle.setText(Integer.toString(SeekBar_DutyCycle.getProgress()) + "%");
			TextView_Frequency.setText(Integer.toString(SeekBar_Frequency.getProgress()) + "Hz");
			
			SeekBar_DutyCycle.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
				@Override
				public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
					TextView_DutyCycle.setText(Integer.toString(SeekBar_DutyCycle.getProgress()) + "%");
					
				}
				
				@Override
				public void onStartTrackingTouch(SeekBar seekBar) {
				
				}
				
				@Override
				public void onStopTrackingTouch(SeekBar seekBar) {
				
				}
			});
			
			SeekBar_Frequency.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
				@Override
				public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
					TextView_Frequency.setText(Integer.toString(SeekBar_Frequency.getProgress()) + "Hz");
				}
				
				@Override
				public void onStartTrackingTouch(SeekBar seekBar) {
				
				}
				
				@Override
				public void onStopTrackingTouch(SeekBar seekBar) {
				
				}
			});
			
			final RadioButton RadioButton_ModeOutput = (RadioButton)view.findViewById(R.id.RadioButton_ModeOutput);
			final RadioButton RadioButton_ModeInput = (RadioButton)view.findViewById(R.id.RadioButton_ModeInput);
			
			if (ArrayList_GPIO_InputOnlyPins.contains(i)){
				RadioButton_ModeOutput.setEnabled(false);
				RadioButton_ModeOutput.setChecked(false);
				RadioButton_ModeOutput.setVisibility(View.GONE);
				RadioButton_ModeInput.setChecked(true);
			}
			
			Button_Apply.setOnClickListener(new View.OnClickListener() {
				@Override
				public void onClick(View v) {
					if (!socket_main.isConnected())
						return;
					OutputStream socketOutputStream = null;
					try {
						socketOutputStream = socket_main.getOutputStream();
						
						ArrayList<Byte> bytes = new ArrayList<Byte>();
						bytes.add((byte)(3 & 0xFF));
						bytes.add((byte)(254 & 0xFF));
						bytes.add((byte)(i & 0xFF));
						
						if (RadioGroup_Mode.getCheckedRadioButtonId() == R.id.RadioButton_ModeInput){
							bytes.add((byte)(1 & 0xFF));
							
							if (RadioGroup_Input.getCheckedRadioButtonId() == R.id.RadioButton_InputDigital){
								bytes.add((byte)(1 & 0xFF));
								
							} else if (RadioGroup_Input.getCheckedRadioButtonId() == R.id.RadioButton_InputAnalog){
								bytes.add((byte)(2 & 0xFF));
								
							} else {
								return;
							}
							
						} else if (RadioGroup_Mode.getCheckedRadioButtonId() == R.id.RadioButton_ModeOutput){
							bytes.add((byte)(2 & 0xFF));
							
							if(RadioGroup_Output.getCheckedRadioButtonId() == R.id.RadioButton_OutputDigital){
								bytes.add((byte)(1 & 0xFF));
								
								if (RadioGroup_OutputDigital.getCheckedRadioButtonId() == R.id.RadioButton_OutputDigital_HIGH){
									bytes.add((byte)(1 & 0xFF));
								} else if (RadioGroup_OutputDigital.getCheckedRadioButtonId() == R.id.RadioButton_OutputDigital_LOW){
									bytes.add((byte)(0 & 0xFF));
								} else {
									return;
								}
								
							} else if (RadioGroup_Output.getCheckedRadioButtonId() == R.id.RadioButton_OutputPWM){
								bytes.add((byte)(2 & 0xFF));
								bytes.add((byte)(SeekBar_DutyCycle.getProgress() & 0xFF));
								//bytes.add((byte)(SeekBar_Frequency.getProgress() & 0xFF));
							} else {
								return;
							}
							
						} else {
							return;
						}
						
						bytes.set(0, (byte)((bytes.size()-1) & 0xFF));
						
						byte[] bytes1 = new byte[bytes.size()];
						for(int i=0; i<bytes.size();i++){
							bytes1[i] = bytes.get(i);
						}
						
						Log.d("Send:", bytes.toString());
						
						socketOutputStream.write(bytes1);
						
					} catch (IOException e) {
						Log.d("ERROR", e.getMessage());
						e.printStackTrace();
					}
				}
			});
			
			linearLayout.addView(view);
		}
		
	}
	
	@Override
	public void onBackPressed() {
		
		super.onBackPressed();
		final Socket socket_main = sockets.get("main");
		if (socket_main.isConnected()){
			byte[] bytes = new byte[1];
			bytes[0] = 18;
			Bootloader.send(socket_main, bytes);
		}
		
		//moveTaskToBack(true);
	}
}
