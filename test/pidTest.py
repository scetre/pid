from pid.pid import PID

# Create a new PID instance with the desired parameters
pid = PID(Kp, Ki, Kd, setpoint)

# Update the PID with the current process value and get the control output
output = pid.update(process_value)
