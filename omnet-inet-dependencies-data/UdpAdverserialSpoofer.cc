/*
 * UdpAdverserialSpoofer.cpp
 *
 *  Created on: Aug 1, 2019
 *      Author: poori
 */

#include "UdpAdverserialSpoofer.h"
#include "inet/applications/base/ApplicationPacket_m.h"
#include "inet/applications/udpapp/UdpBasicApp.h"
#include "inet/common/ModuleAccess.h"
#include "inet/common/TagBase_m.h"
#include "inet/common/TimeTag_m.h"
#include "inet/common/lifecycle/ModuleOperations.h"
#include "inet/common/packet/Packet.h"
#include "inet/networklayer/common/FragmentationTag_m.h"
#include "inet/networklayer/common/L3AddressResolver.h"
#include "inet/transportlayer/contract/udp/UdpControlInfo_m.h"
#include "inet/physicallayer/common/packetlevel/SignalTag_m.h"
namespace inet {
Define_Module(UdpAdverserialSpoofer);

UdpAdverserialSpoofer::UdpAdverserialSpoofer() : UdpBasicApp() {
    // TODO Auto-generated constructor stub
}

UdpAdverserialSpoofer::~UdpAdverserialSpoofer() {
    // TODO Auto-generated destructor stub
}

void UdpAdverserialSpoofer::handleMessageWhenUp(cMessage *msg)
{
    UdpBasicApp::handleMessageWhenUp(msg);
}


void UdpAdverserialSpoofer::sendPacket()
{
    std::ostringstream str;
    str << packetName << "-" << numSent;
    Packet *packet = new Packet(str.str().c_str());
    if(dontFragment)
        packet->addTagIfAbsent<FragmentationReq>()->setDontFragment(true);
    const auto& payload = makeShared<ApplicationPacket>();
    payload->setChunkLength(B(par("messageLength")));

    //payload->setSequenceNumber(numSent);
    payload->setSequenceNumber(1400);
    payload->addTag<CreationTimeTag>()->setCreationTime(simTime());
    packet->insertAtBack(payload);
    L3Address destAddr = chooseDestAddr();

    packet->addTag<SignalPowerReq>()->setPower(W(10));
    emit(packetSentSignal, packet);
    socket.sendTo(packet, destAddr, destPort);
    numSent++;
}
//
void UdpAdverserialSpoofer::processPacket(Packet *pk)
{
    UdpBasicApp::processPacket(pk);
}


} /* namespace inet */
