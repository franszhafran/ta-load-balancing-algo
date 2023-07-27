/*
 * Title:        CloudSim Toolkit
 * Description:  CloudSim (Cloud Simulation) Toolkit for Modeling and Simulation
 *               of Clouds
 * Licence:      GPL - http://www.gnu.org/copyleft/gpl.html
 *
 * Copyright (c) 2009, The University of Melbourne, Australia
 */


package org.cloudbus.cloudsim.examples;

import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.LinkedList;
import java.util.List;
import java.util.Collections;
import java.util.Comparator;
import java.util.Random;

import org.cloudbus.cloudsim.Cloudlet;
import org.cloudbus.cloudsim.CloudletSchedulerSpaceShared;
import org.cloudbus.cloudsim.CloudletSchedulerTimeShared;
import org.cloudbus.cloudsim.Datacenter;
import org.cloudbus.cloudsim.DatacenterBroker;
import org.cloudbus.cloudsim.DatacenterCharacteristics;
import org.cloudbus.cloudsim.Host;
import org.cloudbus.cloudsim.Log;
import org.cloudbus.cloudsim.Pe;
import org.cloudbus.cloudsim.Storage;
import org.cloudbus.cloudsim.UtilizationModel;
import org.cloudbus.cloudsim.UtilizationModelFull;
import org.cloudbus.cloudsim.Vm;
import org.cloudbus.cloudsim.VmAllocationPolicySimple;
import org.cloudbus.cloudsim.VmSchedulerTimeShared;
import org.cloudbus.cloudsim.core.CloudSim;
import org.cloudbus.cloudsim.core.SimEntity;
import org.cloudbus.cloudsim.core.SimEvent;
import org.cloudbus.cloudsim.provisioners.BwProvisionerSimple;
import org.cloudbus.cloudsim.provisioners.PeProvisionerSimple;
import org.cloudbus.cloudsim.provisioners.RamProvisionerSimple;

/**
 * An example showing how to create simulation entities
 * (a DatacenterBroker in this example) in run-time using
 * a globar manager entity (GlobalBroker).
 */
public class CloudSimExampleTAEnhance {

	/** The cloudlet list. */
	private static List<Cloudlet> cloudletList;

	/** The vmList. */
	private static List<Vm> vmList;

	private static List<Vm> createVM(int userId, int vms, int idShift) {
		//Creates a container to store VMs. This list is passed to the broker later
		LinkedList<Vm> list = new LinkedList<Vm>();

		//VM Parameters
		long size = 10000; //image size (MB)
		int ram = 1024; //vm memory (MB)
		int mips = 2000;
		long bw = 1000;
		int pesNumber = 1; //number of cpus
		String vmm = "Xen"; //VMM name

		//create VMs
		Vm[] vm = new Vm[vms];

		for(int i=0;i<2;i++){
			if(i>0) {
				mips = 1000;
			}
			vm[i] = new Vm(idShift + i, userId, mips, pesNumber, ram, bw, size, vmm, new CloudletSchedulerSpaceShared());
			list.add(vm[i]);
		}

		return list;
	}

	private static long randomNumber(long seed) {
		Random rand = new Random(seed);
		return rand.nextLong();
	}

	private static List<Cloudlet> createCloudlet(int userId, int cloudlets, int idShift){
		// Creates a container to store Cloudlets
		LinkedList<Cloudlet> list = new LinkedList<Cloudlet>();

		int pesNumber = 1;
		UtilizationModel utilizationModel = new UtilizationModelFull();

		

		// long[] dataset = {41106L, 51L,43215L, 80L,19821L, 92L,13282L, 80L,39044L, 10L,10481L, 8L,27533L, 8L,27249L, 76L,44548L, 82L,11766L, 80L,12073L, 10L,32929L, 57L,11186L, 10L,36766L, 55L,35740L, 140L,26954L, 29L,24059L, 53L,16354L, 9L,39683L, 8L,30570L, 29L};
		long[] dataset = {41106L, 51L,43215L, 80L,19821L, 92L,13282L, 82L,39044L, 10L};
		Cloudlet[] cloudlet = new Cloudlet[dataset.length/2];
		for(int i=0;i<dataset.length/2;i++) {
			long samenumber = dataset[i*2];
			int dl = (int) dataset[(i*2)+1];
			long length = samenumber;
			long fileSize = samenumber;
			long outputSize = samenumber;
			cloudlet[i] = new Cloudlet(idShift + i, length, pesNumber, fileSize, outputSize, utilizationModel, utilizationModel, utilizationModel);
			// setting the owner of these Cloudlets
			cloudlet[i].setUserId(userId);
			cloudlet[i].setDeadline(dl);
			list.add(cloudlet[i]);
			Log.printLine(String.format("%d, %d, %d", idShift+i+1, length, dl));
		}

		return list;
	}

	public static void schedule(DatacenterBroker broker, List<Cloudlet> cloudlets, List<Vm> vms) {
		Comparator<Cloudlet> sortByLength = new Comparator<Cloudlet>() {
			@Override
			public int compare(Cloudlet cloudlet1, Cloudlet cloudlet2) {
				return (int) (cloudlet1.getDeadline() - cloudlet2.getDeadline());
			}
		};
		Collections.sort(cloudlets, sortByLength);
		float[] readyAt = new float[vms.size()];
		for(int i= 0; i < cloudlets.size(); i++) {
			Cloudlet cloudlet = cloudlets.get(i);
			
			int decisionIndex = 0;
			float bestScore = 10000;
			float choosenExecutionTime = 0;
			int hasNoPenaltyDecision = 0;
			for(int j=0; j < vms.size(); j++) {
				Vm vm = vms.get(j);
				float executionTime = cloudlet.getCloudletLength()/(float) vm.getMips();
				float vmReadyAt = readyAt[j] + executionTime;
				if(vmReadyAt < cloudlet.getDeadline()) {
					decisionIndex = j;
					choosenExecutionTime = executionTime;
					hasNoPenaltyDecision = 1;
				}
				if(bestScore > vmReadyAt-cloudlet.getDeadline() && hasNoPenaltyDecision == 0) {
					bestScore = vmReadyAt-cloudlet.getDeadline();
					decisionIndex = j;
					choosenExecutionTime = executionTime;
				}
			}
			Vm vm = vms.get(decisionIndex);
			cloudlet.setClassType(i+1);
			broker.bindCloudletToVm(cloudlet.getCloudletId(), vm.getId());
			Log.printLine("Bind cloudlet " + cloudlet.getCloudletId() + " to " + vm.getId() + "" + " with execution time " + choosenExecutionTime + " and deadline " + cloudlet.getDeadline());
			
			readyAt[decisionIndex] += choosenExecutionTime;
			Log.printLine("Ready at status");
			Log.printLine(readyAt[0] + " " + readyAt[1]);
		}
	}


	////////////////////////// STATIC METHODS ///////////////////////

	/**
	 * Creates main() to run this example
	 */
	public static void main(String[] args) {
		Log.printLine("Starting CloudSimExample8...");

		try {
			// First step: Initialize the CloudSim package. It should be called
			// before creating any entities.
			int num_user = 2;   // number of grid users
			Calendar calendar = Calendar.getInstance();
			boolean trace_flag = false;  // mean trace events

			// Initialize the CloudSim library
			CloudSim.init(num_user, calendar, trace_flag);

			GlobalBroker globalBroker = new GlobalBroker("GlobalBroker");

			// Second step: Create Datacenters
			//Datacenters are the resource providers in CloudSim. We need at list one of them to run a CloudSim simulation
			@SuppressWarnings("unused")
			Datacenter datacenter0 = createDatacenter("Datacenter_0");
			@SuppressWarnings("unused")
			Datacenter datacenter1 = createDatacenter("Datacenter_1");

			//Third step: Create Broker
			DatacenterBroker broker = createBroker("Broker_0");
			int brokerId = broker.getId();

			//Fourth step: Create VMs and Cloudlets and send them to broker
			vmList = createVM(brokerId, 6, 0); //creating 5 vms
			cloudletList = createCloudlet(brokerId, 20, 0); // creating 10 cloudlets

			broker.submitVmList(vmList);
			broker.submitCloudletList(cloudletList); 
			
			schedule(broker, cloudletList, vmList);

			// Fifth step: Starts the simulation
			CloudSim.startSimulation();

			// Final step: Print results when simulation is over
			List<Cloudlet> newList = broker.getCloudletReceivedList();
			// newList.addAll(globalBroker.getBroker().getCloudletReceivedList());

			CloudSim.stopSimulation();

			printCloudletList(newList);

			Log.printLine("CloudSimTA finished!");
		}
		catch (Exception e)
		{
			e.printStackTrace();
			Log.printLine("The simulation has been terminated due to an unexpected error");
		}
	}

	private static Datacenter createDatacenter(String name){

		// Here are the steps needed to create a PowerDatacenter:
		// 1. We need to create a list to store one or more
		//    Machines
		List<Host> hostList = new ArrayList<Host>();

		// 2. A Machine contains one or more PEs or CPUs/Cores. Therefore, should
		//    create a list to store these PEs before creating
		//    a Machine.
		List<Pe> peList1 = new ArrayList<Pe>();

		int mips = 2000;

		// 3. Create PEs and add these into the list.
		//for a quad-core machine, a list of 4 PEs is required:
		peList1.add(new Pe(0, new PeProvisionerSimple(mips))); // need to store Pe id and MIPS Rating
		peList1.add(new Pe(1, new PeProvisionerSimple(mips)));
		peList1.add(new Pe(2, new PeProvisionerSimple(mips)));
		peList1.add(new Pe(3, new PeProvisionerSimple(mips)));

		//Another list, for a dual-core machine
		List<Pe> peList2 = new ArrayList<Pe>();

		peList2.add(new Pe(0, new PeProvisionerSimple(mips)));
		peList2.add(new Pe(1, new PeProvisionerSimple(mips)));

		//4. Create Hosts with its id and list of PEs and add them to the list of machines
		int hostId=0;
		int ram = 16384; //host memory (MB)
		long storage = 1000000; //host storage
		int bw = 10000;

		hostList.add(
    			new Host(
    				hostId,
    				new RamProvisionerSimple(ram),
    				new BwProvisionerSimple(bw),
    				storage,
    				peList1,
    				new VmSchedulerTimeShared(peList1)
    			)
    		); // This is our first machine

		hostId++;

		hostList.add(
    			new Host(
    				hostId,
    				new RamProvisionerSimple(ram),
    				new BwProvisionerSimple(bw),
    				storage,
    				peList2,
    				new VmSchedulerTimeShared(peList2)
    			)
    		); // Second machine

		// 5. Create a DatacenterCharacteristics object that stores the
		//    properties of a data center: architecture, OS, list of
		//    Machines, allocation policy: time- or space-shared, time zone
		//    and its price (G$/Pe time unit).
		String arch = "x86";      // system architecture
		String os = "Linux";          // operating system
		String vmm = "Xen";
		double time_zone = 10.0;         // time zone this resource located
		double cost = 3.0;              // the cost of using processing in this resource
		double costPerMem = 0.05;		// the cost of using memory in this resource
		double costPerStorage = 0.1;	// the cost of using storage in this resource
		double costPerBw = 0.1;			// the cost of using bw in this resource
		LinkedList<Storage> storageList = new LinkedList<Storage>();	//we are not adding SAN devices by now

		DatacenterCharacteristics characteristics = new DatacenterCharacteristics(
                arch, os, vmm, hostList, time_zone, cost, costPerMem, costPerStorage, costPerBw);


		// 6. Finally, we need to create a PowerDatacenter object.
		Datacenter datacenter = null;
		try {
			datacenter = new Datacenter(name, characteristics, new VmAllocationPolicySimple(hostList), storageList, 0);
		} catch (Exception e) {
			e.printStackTrace();
		}

		return datacenter;
	}

	//We strongly encourage users to develop their own broker policies, to submit vms and cloudlets according
	//to the specific rules of the simulated scenario
	private static DatacenterBroker createBroker(String name){

		DatacenterBroker broker = null;
		try {
			broker = new DatacenterBroker(name);
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		}
		return broker;
	}

	/**
	 * Prints the Cloudlet objects
	 * @param list  list of Cloudlets
	 */
	private static void printCloudletList(List<Cloudlet> list) {
		int size = list.size();
		int penaltyTaskCount = 0;
		double penalty = 0;
		double makespan = 0;
		double execution_time = 0;
		Collections.sort(list, new Comparator<Cloudlet>() {
			@Override
			public int compare(Cloudlet arg0, Cloudlet arg1) {
				if(arg0.getVmId() < arg1.getVmId()) {
					return -1;
				}
				return 1;
			}
		});
		Cloudlet cloudlet;

		String indent = "    ";
		Log.printLine();
		Log.printLine("========== OUTPUT ==========");
		Log.printLine(
				"Cloudlet ID" 
				+ indent + "STATUS" 
				+ indent + "Data center ID" 
				+ indent + "VM ID" 
				+ indent + indent + "Time" 
				+ indent + "Start Time" 
				+ indent + "Finish Time" 
				+ indent + "Deadline"  
				+ indent + indent + "Length"
				+ indent + "Penalty (y/n)");

		DecimalFormat dft = new DecimalFormat("###.##");
		List<List<Integer>> scheduleList = new ArrayList<>();
		for(int i = 0; i <8;i++) {
			List<Integer> test = new ArrayList<>();
			scheduleList.add(test);
		}
		for (int i = 0; i < size; i++) {
			cloudlet = list.get(i);
			Log.print(indent + cloudlet.getCloudletId() + indent + indent);

			if (cloudlet.getCloudletStatus() == Cloudlet.SUCCESS){
				Log.print("SUCCESS");
				String penaltyStr = "no";
				if(cloudlet.getFinishTime() > cloudlet.getDeadline()) {
					penalty += cloudlet.getFinishTime() - (cloudlet.getDeadline());
					penaltyStr = "yes";
				}
				Log.printLine( indent + indent + cloudlet.getResourceId() + indent + indent + indent + cloudlet.getVmId() +
						indent + indent + indent + dft.format(cloudlet.getActualCPUTime()) +
						indent + indent + dft.format(cloudlet.getExecStartTime())+ 
						indent + indent + indent + dft.format(cloudlet.getFinishTime()) + 
						indent + indent + indent + cloudlet.getDeadline() +
						indent + indent + indent + cloudlet.getCloudletLength() +
						indent + indent + indent + penaltyStr);
				if(makespan < cloudlet.getFinishTime()) {
					makespan = cloudlet.getFinishTime();
					penaltyTaskCount += 1;
				}
				execution_time = execution_time + cloudlet.getActualCPUTime();
				List<Integer> vmSchedule = scheduleList.get(cloudlet.getVmId());
				vmSchedule.add(cloudlet.getCloudletId() + 1);
			}
		}
		for(int i=0; i< scheduleList.size() ;i ++) {
			for(int j=0; j< scheduleList.get(i).size() ;j ++) {
				Log.print(scheduleList.get(i).get(j) + ",");
			}
			Log.printLine();
		}
		Log.printLine("Total penalty " + penalty);
		Log.printLine("Total penalty count " + penaltyTaskCount);
		Log.printLine("Makespan " + makespan);
		Log.printLine("Execution Time " + execution_time);
		Log.printLine("Resource utilization " + execution_time*100/(makespan*6));
	}

	public static class GlobalBroker extends SimEntity {

		private static final int CREATE_BROKER = 0;
		private List<Vm> vmList;
		private List<Cloudlet> cloudletList;
		private DatacenterBroker broker;

		public GlobalBroker(String name) {
			super(name);
		}

		@Override
		public void processEvent(SimEvent ev) {
			switch (ev.getTag()) {
			case CREATE_BROKER:
				setBroker(createBroker(super.getName()+"_"));

				//Create VMs and Cloudlets and send them to broker
				setVmList(createVM(getBroker().getId(), 5, 100)); //creating 5 vms
				setCloudletList(createCloudlet(getBroker().getId(), 10, 100)); // creating 10 cloudlets

				broker.submitVmList(getVmList());
				broker.submitCloudletList(getCloudletList());

				CloudSim.resumeSimulation();

				break;

			default:
				Log.printLine(getName() + ": unknown event type");
				break;
			}
		}

		@Override
		public void startEntity() {
			Log.printLine(super.getName()+" is starting...");
			schedule(getId(), 200, CREATE_BROKER);
		}

		@Override
		public void shutdownEntity() {
		}

		public List<Vm> getVmList() {
			return vmList;
		}

		protected void setVmList(List<Vm> vmList) {
			this.vmList = vmList;
		}

		public List<Cloudlet> getCloudletList() {
			return cloudletList;
		}

		protected void setCloudletList(List<Cloudlet> cloudletList) {
			this.cloudletList = cloudletList;
		}

		public DatacenterBroker getBroker() {
			return broker;
		}

		protected void setBroker(DatacenterBroker broker) {
			this.broker = broker;
		}

	}

}
