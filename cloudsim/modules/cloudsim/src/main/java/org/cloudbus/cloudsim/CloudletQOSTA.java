/*
 * Title:        CloudSim Toolkit
 * Description:  CloudSim (Cloud Simulation) Toolkit for Modeling and Simulation of Clouds
 * Licence:      GPL - http://www.gnu.org/copyleft/gpl.html
 *
 * Copyright (c) 2009-2012, The University of Melbourne, Australia
 */
package org.cloudbus.cloudsim;

import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

import org.cloudbus.cloudsim.core.CloudSim;

/**
 * Cloudlet is an extension to the cloudlet. It stores, despite all the
 * information encapsulated in the Cloudlet, the ID of the VM running it.
 *
 * @author Rodrigo N. Calheiros
 * @author Anton Beloglazov
 * @since CloudSim Toolkit 1.0
 * @todo The documentation is wrong. Cloudlet isn't extending any class.
 */
public class CloudletQOSTA extends Cloudlet {
    private int deadline;

    public CloudletQOSTA(
        final int cloudletId,
        final long cloudletLength,
        final int pesNumber,
        final long cloudletFileSize,
        final long cloudletOutputSize,
        final UtilizationModel utilizationModelCpu,
        final UtilizationModel utilizationModelRam,
        final UtilizationModel utilizationModelBw) {
            super(
                cloudletId,
                cloudletLength,
                pesNumber,
                cloudletFileSize,
                cloudletOutputSize,
                utilizationModelCpu,
                utilizationModelRam,
                utilizationModelBw
            );
    }

    public int getDeadline() {
        return this.deadline;
    }

    public void setDeadline(int deadline) {
        this.deadline = deadline;
    }
}
