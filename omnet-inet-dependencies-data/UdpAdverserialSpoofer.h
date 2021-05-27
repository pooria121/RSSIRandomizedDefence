/*
 * UdpAdverserialSpoofer.h
 *
 *  Created on: Aug 1, 2019
 *      Author: poori
 */

#ifndef INET_APPLICATIONS_UDPAPP_UDPADVERSERIALSPOOFER_H_
#define INET_APPLICATIONS_UDPAPP_UDPADVERSERIALSPOOFER_H_

#include <vector>

#include "inet/common/INETDefs.h"

#include "inet/applications/base/ApplicationBase.h"
#include "inet/transportlayer/contract/udp/UdpSocket.h"
#include "inet/applications/udpapp/UdpBasicApp.h"

namespace inet {

class INET_API UdpAdverserialSpoofer : public UdpBasicApp{
 protected:
   virtual void handleMessageWhenUp(cMessage *msg) override;

   // chooses random destination address
   virtual void sendPacket() override;
   virtual void processPacket(Packet *msg) override;



public:
    UdpAdverserialSpoofer();
    virtual ~UdpAdverserialSpoofer();
};

} /* namespace inet */

#endif /* INET_APPLICATIONS_UDPAPP_UDPADVERSERIALSPOOFER_H_ */
